const app = getApp()
Page({
  data: {
    tname: ['自营商品', '代售商品', '其它商品'],
    banner: '',
    products: [],
  },
  onShow: function (option) {
    wx.setNavigationBarTitle({
      title: '商城',
    })
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/openimg?isbanner=True',
      success: function (res) {
        self.setData({
          banner: res.data
        });
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/productlist?onsale=1',
      success: function (res) {
        self.setData({
          products: res.data
        });
      }
    })
  },
  enterdetail: function(event) {
    wx.navigateTo({
      url: '../detail/cityDetail?id=' + event.currentTarget.id
    })
  },
  onShareAppMessage: function () {
    return {
      title: '快来看看爱妙客的电子商城，好东西真多！',
      success: function (res) {
        wx.showToast({
          title: '谢谢分享',
        })
      }
    }
  }
})
