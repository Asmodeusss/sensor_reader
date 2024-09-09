<template>
  <div style="margin:50px">
    <div style="display: flex; flex-wrap: wrap">
      <button v-for="x in metric_categories"
        @click="setReadingId(x.M_ID); chosen_metric=x"> {{ strCleanse(x.Name) }} </button>
    </div>

    <div v-if="chosen_metric" class="chosen_metric_description">
      <div>ID: {{ chosen_metric.M_ID }}</div>
      <div>Name: {{ strCleanse(chosen_metric.Name) }}</div>
      <div>Measurement: {{ strCleanse(chosen_metric.Selected_name) }}</div>
      <div>Precision: {{ chosen_metric.Selected_precision }}</div> 
    </div>

    <table class="reading_table">
      <tr>
        <th @click="setReadingOrder('Sensor_Name')" class="prevent-select">Sensor {{ sortedIndicator("Sensor_Name") }}</th>
        <th @click="setReadingOrder('Sensor_Model')" class="prevent-select">Model {{ sortedIndicator("Sensor_Model") }}</th>
        <th @click="setReadingOrder('V')" class="prevent-select">value {{ sortedIndicator("V") }}</th>
        <th @click="setReadingOrder('T')" class="prevent-select">time {{ sortedIndicator("T") }}</th>
      </tr>
      <tr>
        <!-- <th><p>Message is: {{ message }}</p> -->
          <th> <input v-model="sensor_filter_value" placeholder="filter by sensor" class="filter_input"/> </th>
          <th> <input v-model="model_filter_value" placeholder="filter by model" class="filter_input"/> </th>
          <th> <input v-model="reading_filter_value" placeholder="filter by value" class="filter_input"/> </th>
          <th> <input v-model="time_filter_value" placeholder="filter by time" class="filter_input"/> </th>
      </tr>
      <tr v-if="reading_data.length" v-for="x in filteredReadingData"> 
        <td >{{ x.Sensor_Name }}</td>
        <td >{{ x.Sensor_Model }}</td>
        <td >{{ x.V }}</td>
        <td >{{ x.T }}</td>
      </tr>
    </table>
    <!-- this component is in case there is a metric with no entries, but that didnt end up being the case -->
    <!-- <div v-if="!reading_data.length" class="no_data_panel"> NO DATA</div> -->
  </div>
</template>

<script>

  import _ from 'lodash';
  import axios from 'axios'

  export default {
    data() {
      return {
        toggleValue: true,

        sensor_filter_value: "",
        model_filter_value: "",
        reading_filter_value: "",
        time_filter_value: "",

        metric_categories: [],
        chosen_metric: {},

        sensor_types: {},
        sensor_data: [],

        reading_data: [],
        reading_sort_category: { id: "Sensor_Name ", order: "asc"}
      }
    },

    methods: {

      async getMetricData(id = 0) {

        var params = {
          params: {
            "m_id": id
          }
        }

        var data = await axios.get("http://127.0.0.1:8000/api/getMetricData/", params );
        //console.log(data["data"])
        this.reading_data = data["data"]
        return data["data"]
      },

      async populateSensorTypes() {
        var data = await axios.get("http://127.0.0.1:8000/api/getSensorMake/", {})
        for(var i in data["data"]) {
          var t = data["data"][i]["S_Id"]
          var v = data["data"][i]["S_Variant"]
          var name = data["data"][i]["S_Name"]
          if (t in this.sensor_types) {
            this.sensor_types[t][v]=name
          } else {
            this.sensor_types[t]={}
            this.sensor_types[t][v]=name
          }
        }
      },

      getSensorName(t, v) {
        var ret = "UNDEFINED"
        if(t in this.sensor_types){
          if(v in this.sensor_types[t]){
            ret = this.sensor_types[t][v]
          }
        }
        return ret
      },

      async getSensorType(t=0, v=0) {
        var params = {
          params: {
            "sensor_type": t,
            "sensor_variant": v
          }
        }

        var data = await axios.get("http://127.0.0.1:8000/api/getSensorMake/", params)
        //console.log(data["data"])
        return Array(data["data"])
      },

      async getSensorData(s_id) {
        var params = {
          params: {
            "sensor_id": s_id,
          }
        }

        var data = await axios.get("http://127.0.0.1:8000/api/getSensor/", params)
        return data["data"]

      },

      async getMetrics() {
        var params = {
          params: {
            "type": "all",
          }
        }

        var data = await axios.get("http://127.0.0.1:8000/api/getMetrics/", params)
        this.metric_categories = data["data"]
        //console.log(data["data"])
        return data["data"]
      },

      setReadingOrder(s) {
        var revorder = { 'asc': 'desc', 'desc': 'asc'}
        if (this.reading_sort_category.id == s) {
          this.reading_sort_category = { id: s, order: revorder[this.reading_sort_category.order]}
        } else {
          this.reading_sort_category = {
            id: s,
            order: 'asc'
          }
        }
      },
      
      setReadingId(m_id) {
        this.reading_data = this.getMetricData(m_id).finally(this.afterDone)
      },

      // In cases where sensors end with a number, fix it to add extra zeroes.
      // Kind of a bad way to do it. Depends on if its ok that Sensor 2 comes after Sensor 19 when sorting.
      // The reason this could be better is because there might be sensors with different naming conventions.
      fixSensorName(name) {
        if (name == "UNDEFINED") return name

        var at = name.lastIndexOf(" ")
        var part1= name.slice(0, at)
        var part2= name.slice(at +1)

        //console.log(part1)
        //console.log(part2)
        
        while(part2.length <3){
          part2 = "0" + part2
        }

        return(part1 + " " + part2)


      },

      //The reason this is here is due to two tables being combined into one
      async afterDone() {
        for(var i in this.reading_data){
          var sensor = await this.getSensorData(this.reading_data[i].Sensor_ID);
          //console.log("sensor json")
          //console.log(sensor)
          var obj = JSON.parse(sensor.replace(/'/g,'"'))
          var t = obj["Sensor_Type"]
          var v = obj["Sensor_Variant"]
          this.reading_data[i]["Sensor_Model"] = this.getSensorName(t, v)
          this.reading_data[i]["Sensor_Name"] = this.fixSensorName(obj["Sensor_Name"])

        }
      },

      strCleanse(s) {
        //I did not have the time to fix encoding so this is a shorthand fix for it. 
        //I know, I found it too annoying but after nearly 2 hours I realized I was wasting too much time
        //Yes, the DB/JS/request encoding should be more properly looked into
        return s.replace("â‚‚","₂").replace("Â","").replace("Â","")
      },  

      onLoad() {
        this.populateSensorTypes()
        this.sensor_types = this.getSensorType()
        this.metric_categories = this.getMetrics()
        this.chosen_metric = this.metric_categories[1]
      
        this.getSensorData(3145829)
      },

      sortedIndicator(t) {
        if (this.reading_sort_category["id"]==t) {
          if (this.reading_sort_category["order"]=='asc') {
            return "▴"
          }
          else {
            return "▾"
          }
        }
      }

    },

    computed: {
      orderedReadingData: function() {
        return _.orderBy(this.reading_data, [this.reading_sort_category.id], [this.reading_sort_category.order])
      },

      filteredReadingData: function() {
        var l = this.orderedReadingData
        var final = []

        for (var i in l){
          var good = true
          if (this.sensor_filter_value != ""){
            if(!String(l[i]["Sensor_Name"]).startsWith(this.sensor_filter_value)) {good = false}
          }

          if (this.model_filter_value != ""){
            if(!String(l[i]["Sensor_Model"]).startsWith(this.model_filter_value)) {good = false}
          }

          if (this.reading_filter_value != ""){
            if(!String(l[i]["V"]).startsWith(String(this.reading_filter_value))) {good = false}
          }

          if (this.time_filter_value != ""){
            if (!String(l[i]["T"]).startsWith(String(this.time_filter_value))) {good = false}
          }
          
          if(good){
            final.push(l[i])
          }
        }
        return final
      }
    },

    beforeMount() {
      this.onLoad()
    }
  }
</script>

<style scoped>

body {
  font-family:monospace;
}

th {
  background-color: gray;
}

.reading_table{
  width: 100%
}

.reading_table > tr >th{
  background-color: aliceblue;
  width: 200px;

}

.chosen_metric_description {
  background-color: beige;
}

.filter_input {
  width:100%
}

.no_data_panel {
  text-align: center;
  width: 100%;
  padding: 100px;
  font-size: 30px;
  background-color: beige;
  transition: 0.5ms;
}

.prevent-select {
  -webkit-user-select: none; /* Safari */
  -ms-user-select: none; /* IE 10 and IE 11 */
  user-select: none; /* Standard syntax */
}
</style>
