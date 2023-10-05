const app = getApp()

Page({
  data: {
    userInfo: {},
    authed: 0,
    balance: 0,
    backimg: '',
  },
  onShow: function () {
    wx.setNavigationBarTitle({
      title: '我的'
    })
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=0',
      success: function (res) {
        self.setData({
          'backimg': res.data,
          'authed': wx.getStorageSync('authed'),
          'userInfo': wx.getStorageSync('userinfo'),
        });
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/userdetail?userid=' + wx.getStorageSync('userid'),
      success: function (res) {
        self.setData({
          balance: res.data[0].fields.balance.toFixed(2),
        })
      }
    })
  },
  doauth: function(e) {
    var self=this
    if (e.detail.userInfo) {
      wx.login({
        success: res1 => {
          wx.getUserInfo({
            success: res2 => {
              var u = res2.userInfo
              wx.setStorageSync('userinfo', u)
              self.setData({'userInfo': u,})
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
                  wx.setStorageSync('userid', res.data.userid)
                  wx.setStorageSync('token', res.data.token)
                  self.setData({ 'authed': 1 })
                  wx.setStorageSync('authed', 1)
                }
              })
            },
          })
        }
      })
    }
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
  mypay: function () {
    wx.request({
      url: app.globalData.apiURL + '/paylist',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        mode: 'mypay',
      },
      method: 'POST',
      success: function (res) {
        var mypay=''
        for (var i in res.data) {
          if (res.data[i].fields.amount > 0) {
            mypay += res.data[i].fields.date.split("T")[0] + ' 充值金额：' + res.data[i].fields.amount + '\r\n'
          }
        }
        wx.showModal({
          title: '充值记录',
          content: mypay,
        })
      }
    })
  },
  mypromot: function () {
    wx.request({
      url: app.globalData.apiURL + '/paylist',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        mode: 'mypromot',
      },
      method: 'POST',
      success: function (res) {
        //console.log(res.data)
        var mypromot = ''
        for (var i in res.data) {
          if (res.data[i].fields.amount>0) {
            mypromot += res.data[i].fields.date.split("T")[0] + ' 充值金额：' + res.data[i].fields.amount + '\r\n'
          }
        }
        wx.showModal({
          title: '成功的推广',
          content: mypromot,
        })
      }
    })
  },
  onShareAppMessage: function (res) {
    return {
      title: '妙纯酸奶优惠充值，充得多送得多',
      path: 'pages/experience/showAll?&memberid=' + wx.getStorageSync('userid'),
      imageUrl: 'http://wx3.sinaimg.cn/mw690/0068B7ATly1fzd1ns1767j31900u0u0x.jpg'
    }
  },
  question: function () {
    wx.navigateTo({
      url: '../question/question'
    })
  },
})
