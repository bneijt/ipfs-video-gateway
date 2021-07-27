var app = new Vue({
  el: '#app',
  data () {
    return {
        pinned: [
        ],
        cidToPin: '',
        lastPinResponse: ''
      };
  },
  methods: {
      pinReload: function() {
        this.lastPinResponse = 'Reloading...';
        axios
          .get('/api/v0/pin/ls', { params: {
            type: 'recursive'
          }})
          .then(response => {this.lastPinResponse = response.statusText; this.pinned = response.data})
          .catch(error => (this.lastPinResponse = error.response.statusText));
      }
  },
  mounted () {
    this.pinReload();
  }
})
