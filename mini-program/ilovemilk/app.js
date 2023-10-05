//app.js
App({
  onLaunch: function () {
    var self = this
    this.userlogin()
    wx.getLocation({
      type: 'wgs84',
      success: function (res) {
        wx.setStorageSync('latitude', res.latitude)
        wx.setStorageSync('longitude', res.longitude)
      },
    })
  },
  userlogin: function () {
    var self = this
    wx.login({
      success: res1 => {
        if (res1.code) {
          wx.getUserInfo({
            success: res2 => {
              var u = res2.userInfo
              this.globalData.userInfo = u
              var ranges = [
                '\ud83c[\udf00-\udfff]',
                '\ud83d[\udc00-\ude4f]',
                '\ud83d[\ude80-\udeff]'
              ];
              var namestr = u.nickName.replace(new RegExp(ranges.join('|'), 'g'), '');
              wx.request({
                url: self.globalData.apiURL + '/userlogin',
                data: {
                  code: res1.code,
                  name: namestr,
                  pic: u.avatarUrl,
                  detail: u.country+u.province+u.city+"_"+u.gender,
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
      }
    })
  },
  globalData: {
    userInfo: null,
    apiURL: 'https://weixinpt.sinaapp.com/bg_xb'
  }
})
