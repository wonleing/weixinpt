const app = getApp();
Page({
  data: {
    bootimg: '',
    leftValue: -150,
    animationData: {}
  },
  startProject: function () {
    var self = this
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.userInfo']) {
          wx.authorize({ scope: 'scope.userInfo', })
        }
        if (!res.authSetting['scope.address']) {
          wx.authorize({ scope: 'scope.address', })
        }
      }
    })
    wx.login({
      success: res1 => {
        wx.getUserInfo({
          success: res2 => {
            var u = res2.userInfo
            app.globalData.userInfo = u
            var ranges = [
              '\ud83c[\udf00-\udfff]',
              '\ud83d[\udc00-\ude4f]',
              '\ud83d[\ude80-\udeff]'
            ];
            var namestr = u.nickName.replace(new RegExp(ranges.join('|'), 'g'), '');
            wx.request({
              url: app.globalData.apiURL + '/userlogin',
              data: {
                code: res1.code,
                name: namestr,
                pic: u.avatarUrl,
                detail: u.country + u.province + u.city + "_" + u.gender,
              },
              success: function (res) {
                //console.log(res)
                wx.setStorageSync('userid', res.data.userid)
                wx.setStorageSync('token', res.data.token)
              }
            })
          },
        })
      }
    })
    wx.switchTab({
      url: '../experience/enterSubject'
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    const self = this;
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=0',
      success: function (res) {
        self.setData({ bootimg: res.data });
      }
    });
    wx.setNavigationBarTitle({
      title: '妙纯食品',
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
})
 
