const app = getApp();
Page({
  data: {
    bootimg: '',
    leftValue: -150,
    animationData: {}
  },
  startProject: function () {
    wx.switchTab({
      url: '../experience/experience'
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    const self = this;
    wx.request({
      url: app.globalData.apiURL + '/openimg',
      success: function (res) {
        self.setData({ bootimg: res.data });
      }
    });
    wx.setNavigationBarTitle({
      title: '爱妙客',
    });
    this.animation = wx.createAnimation({timingFunction: 'linear'});
    this.animation.translate(this.data.leftValue).step({ duration: 6000 });
    this.animation.translate(0).step({ duration: 6000 });
    this.animation.translate(this.data.leftValue).step({ duration: 6000 });
    this.animation.translate(0).step({ duration: 6000 });
    this.animation.translate(this.data.leftValue).step({ duration: 6000 });
    this.animation.translate(0).step({ duration: 6000 });
    this.setData({
      animationData: this.animation.export()
    });
  },
  onShareAppMessage: function () {
    return {
      title: '爱妙客--Ilovemilk官方电子展商平台',
      success: function (res) {
        wx.showToast({
          title: '谢谢分享',
        })
      }
    }
  }
})
 
