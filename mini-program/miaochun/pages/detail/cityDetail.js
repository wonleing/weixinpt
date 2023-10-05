const app = getApp()
Page({
  data: {
    indicatorDots: false,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    productinfo:{},
    productid: '',
    count: 0, //numbers of buying
    total: 0, //cost of money
    balance: 0, //money you have
    province: '',
    city: '',
    county: '',
    address: '',
    username: '',
    usertel: '',
    comments: [],
    videoURL: '',
    morecomment: 0,
    authed: 0,
    backimg: '',
  },
  onLoad: function (options) {
    wx.setNavigationBarTitle({
      title: '产品详情'
    })
    if (options.memberid) {
      wx.setStorageSync('memberid', options.memberid)
    }
    const self = this
    const pid = options.id;
    wx.request({
      url: app.globalData.apiURL + '/productlist?productid='+pid,
      success: function (res) {
        if (res.data[0].fields.pic.endsWith(".mp4")) {
          self.setData({ videoURL: morepic })
        }
        self.setData({
          productinfo: res.data[0],
          productid: pid,
          slidelist: res.data[0].fields.pic.split(','),
          detaillist: res.data[0].fields.otherpic.split(','),
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=4',
      success: function (res) {
        self.setData({
          comments: res.data,
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=0',
      success: function (res) {
        self.setData({
          'backimg': res.data,
          'authed': wx.getStorageSync('authed'),
        });
      }
    })
  },
  onShow: function() {
    if (wx.getStorageSync('userid') > 0) {
      this.refreshbalance()
    }
  },
  refreshbalance: function () {
    var self = this
    wx.request({
      url: app.globalData.apiURL + '/userdetail?userid=' + wx.getStorageSync('userid'),
      success: function (res) {
        self.setData({
          balance: res.data[0].fields.balance.toFixed(2),
        })
      }
    })
  },
  selectaddr: function () {
    var self = this
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.address']) {
          wx.authorize({ scope: 'scope.address', })
        }
      }
    })
    wx.chooseAddress({
      success: function (res) {
        self.setData({
          province: res.provinceName,
          city: res.cityName,
          county: res.countyName,
          address: res.detailInfo,
          username: res.userName,
          usertel: res.telNumber,
        })
      }
    })
  },
  reducecount: function () {
    if (this.data.count > 0) {
      this.data.count -= 1
      this.setData({
        count: this.data.count
      })
    }
    this.dosum()
  },
  addcount: function () {
    this.data.count = this.data.count + 1;
    this.setData({
      count: this.data.count
    })
    this.dosum()
  },
  dosum: function () {
    var total = this.data.productinfo.fields.price * this.data.count
    this.setData({
      total: total,
      orders: [{ 'productid': this.data.productinfo.pk, 'number': this.data.count }]
    })
  },
  dopay: function (e) {
    var self = this
    if (this.data.count < 1) {
      wx.showToast({
        title: '请选数量',
      })
      return -1
    }
    if (this.data.address == '') {
      wx.showToast({
        title: '请填地址',
      })
      return -1
    }
    if (this.data.total > this.data.balance) {
      wx.request({
        url: app.globalData.apiURL + '/payable',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          memberid: wx.getStorageSync('memberid'),
          amount: this.data.total - this.data.balance,
        },
        method: 'POST',
        success: function (res1) {
          //console.log(res1)
          wx.requestPayment({
            'timeStamp': res1.data.timeStamp,
            'nonceStr': res1.data.nonceStr,
            'package': res1.data.package,
            'signType': res1.data.signType,
            'paySign': res1.data.paySign,
            'success': function (res2) {
              self.makeorder()
            },
            'fail': function (res2) {
              wx.showToast({ title: '支付取消', })
            }
          })
        },
      })
    } else {
      self.makeorder()
    }
  },
  makeorder: function() {
    var self = this
    wx.request({
      url: app.globalData.apiURL + '/makeorder',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        productid: this.data.productid,
        amount: this.data.count,
        province: this.data.province,
        city: this.data.city,
        county: this.data.county,
        address: this.data.address,
        username: this.data.username,
        usertel: this.data.usertel,
      },
      method: 'POST',
      success: function (res) {
        if (res.data=='order completed') {
          wx.showModal({
            title: '下单成功',
            content: '你可在我的订单中查看或取消',
            success (res1) {
              if (res1.confirm) {
                wx.navigateTo({
                  url: '../myself/myOrder',
                })
              }
            }
          })
          self.refreshbalance()
        } else {
          console.log(res.data)
          wx.showToast({
            title: '库存不足',
          })
        }
      }
    })
  },
  payroll: function () {
    wx.switchTab({
      url: '../payticket/orderDetail',
    })
  },
  comment: function (e) {
    var self = this
    if (e.detail.value.content == '') {
      wx.showToast({
        title: '请写内容',
      })
    } else {
      wx.request({
        url: app.globalData.apiURL + '/comment',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          content: e.detail.value.content,
        },
        method: 'POST',
        success: function (res) {
          wx.showToast({
            title: '评论成功',
          })
          self.refreshbalance()
        }
      })
    }
  },
  showmore: function () {
    this.setData({ morecomment: 1 })
  },
  doauth: function (e) {
    var self = this
    if (e.detail.userInfo) {
      wx.login({
        success: res1 => {
          wx.getUserInfo({
            success: res2 => {
              var u = res2.userInfo
              wx.setStorageSync('userinfo', u)
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
                  self.onShow()
                }
              })
            },
          })
        }
      })
    }
  },
  onShareAppMessage: function () {
    return {
      title: '发现好货：'+this.data.productinfo.fields.title,
      success: function (res) {
        wx.showToast({
          title: '谢谢分享',
        })
      }
    }
  }
})