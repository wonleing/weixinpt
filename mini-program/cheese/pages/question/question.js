const app = getApp()

Page({
  data: {
    questionList: []
  },
  onLoad: function (option) {
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/qalist',
      success: function (res) {
        self.setData({
          questionList: res.data,
        })
      }
    })
    wx.setNavigationBarTitle({
      title: '常见问题'
    })
  }
})
