//app.js
App({
  onLaunch: function () {
    //var self = this
    // wx.getLocation({
    //   type: 'wgs84',
    //   success: function (res) {
    //     wx.setStorageSync('latitude', res.latitude)
    //     wx.setStorageSync('longitude', res.longitude)
    //   },
    // })
  },
  globalData: {
    apiURL: 'https://weixinpt.sinaapp.com/ebreath'
  }
})
