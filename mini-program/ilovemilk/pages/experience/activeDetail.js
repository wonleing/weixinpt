const app = getApp()

Page({
  data: {
    url: '',
  },
  onLoad: function (option) {
    if (option.url) {
      var URL = option.url
    } else {
      var URL = app.globalData.apiURL + '/forward?aid=' + option.aid
    }
    this.setData({
      url: URL,
    })
    wx.setNavigationBarTitle({
      title: '最新文章',
    })
  }
})