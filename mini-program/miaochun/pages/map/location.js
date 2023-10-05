Page({
  data: {
    lat: '',
    lon: '',
    markers: [],
  },
  onLoad: function (options) {
    this.setData({
      markers: [{
        iconPath: '/images/map.png',
        callout: {
          color: "#888888",
          content: options.lname,
          fontSize: "9",
          borderRadius: "10",
          bgColor: "#ffffff",
          padding: "10",
          display: "ALWAYS"
        },
        latitude: options.lat,
        longitude: options.lon,
        width: 20,
        height: 20
      }],
      lat: options.lat,
      lon: options.lon,
    })
    wx.setNavigationBarTitle({
      title: '地图位置'
    })
  },
})