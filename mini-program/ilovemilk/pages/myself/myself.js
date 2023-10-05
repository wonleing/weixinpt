const app = getApp()

Page({
  data: {
    userInfo: {},
  },
  onLoad: function (option) {
    this.setData({
      userInfo: app.globalData.userInfo,
    })
    wx.setNavigationBarTitle({
      title: '我的'
    })
  },
  bindViewTap: function () {
    var userid = wx.getStorageSync('userid')
    var token = wx.getStorageSync('token')
    console.log(userid+"-"+token)
  },
  myorder: function () {
    wx.navigateTo({
      url: 'myOrder'
    })
  },
  mycompany: function () {
    wx.navigateTo({
      url: '../collect/collect?userid=' + wx.getStorageSync('userid')
    })
  },
  myproduct: function () {
    wx.navigateTo({
      url: '../collect/collectproduct?userid=' + wx.getStorageSync('userid')
    })
  },
  question: function () {
    wx.navigateTo({
      url: '../question/question'
    })
  },
})
