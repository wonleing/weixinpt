// experiene.js
const app = getApp();

Page({
  data: {
    // indicatorDots: true,
    // autoplay: true,
    // interval: 5000,
    // duration: 1000,
    memberlist: [],
    articlelist: [],
    productlist: []
  },
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/productlist?onsale=1&pp=5',
      success: function (res) {
        self.setData({
          productlist: res.data
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/articlelist?pp=5',
      success: function (res) {
        //console.log(res.data)
        self.setData({
          articlelist: res.data
        })
      }
    })
    wx.setNavigationBarTitle({
      title: '发现'
    })
  },
  onPullDownRefresh: function () {
    this.onShow()
  },
  memberDetail: function (e) {
    wx.navigateTo({
      url: '../detail/viewDetail?id='+e.currentTarget.id
    })
  },
  productDetail: function (event) {
    wx.navigateTo({
      url: '../detail/cityDetail?id=' + event.currentTarget.id
    })
  },
  articleDetail: function (event) {
    wx.navigateTo({
      url: 'activeDetail?aid=' + event.currentTarget.id
    })
  },
  adDetail: function (event) {
    wx.navigateToMiniProgram({
      appId: this.data.adlist[0].link,
      success(res) {
        // 打开成功
      }
    })
  },
  enterSubject: function (event) {
    wx.navigateTo({
      url: 'enterSubject?subjectid=' + event.currentTarget.id
    })
  },
  showAll: function (event) {
    wx.navigateTo({
      url: 'activeDetail?url=http://www.gotmilk.com.cn'
    })
  },
  onShareAppMessage: function () {
    return {
      title: '七十客--纯正的美式奶酪',
      success: function (res) {
        wx.showToast({
          title: '谢谢分享',
        })
      }
    }
  }
})
