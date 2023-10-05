const app = getApp()
Page({
  data: {
    banner: '',
    products: [],
  },
  onShow: function (option) {
    wx.setNavigationBarTitle({
      title: '商城',
    })
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=1',
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
      title: '妙纯酸奶，纯天然零添加',
      success: function (res) {
        wx.showToast({
          title: '谢谢分享',
        })
      }
    }
  }
})
