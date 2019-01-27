var app = new Vue({
  el: '#app',
  data () {
    return {
        pinned: [
          {'cid': 'QmU1GSqu4w29Pt7EEM57Lhte8Lce6e7kuhRHo6rSNb2UaC'}
        ],
        cidToPin: '',
        lastPinResponse: ''
      };
  },
  methods: {
      pinAdd: function() {
        this.lastPinResponse = 'Pinning...';
        axios.get('/api/v0/pin/add', { params:{
            arg: this.cidToPin.trim(),
            recursive: true,
            progress: false
          }})
          .then(response => (this.lastPinResponse = response.statusText))
          .catch(error => (this.lastPinResponse = error.response.statusText));
      },
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
