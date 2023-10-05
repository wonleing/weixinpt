const app = getApp()
Page({
  data: {
    hiddenChoosed: true,
    hiddenCity: true,
    hiddenServer: true,
    hiddenCoupon: true,
    hiddenAddCity: true,
    productinfo: {},
    productid: '',
    count: 0, //numbers of buying
    total: 0, //cost of money
    balance: 0, //money you have
    province: '',
    city: '',
    county: '',
    address: '请选择配送地址',
    username: '',
    usertel: '',
    comments: [],
    datestr: '',
    authed: 0,
    backimg: '',
    man: 0,
    postfee: 0,
  },
  onLoad: function (options) {
    var myDate = new Date();
    wx.setNavigationBarTitle({
      title: '产品详情'
    })
    if (options.memberid) {
      wx.setStorageSync('memberid', options.memberid)
    }
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/productlist?productid=' + options.id,
      success: function (res) {
        self.setData({
          productinfo: res.data[0].fields,
          productid: options.id,
          slidelist: res.data[0].fields.pic.split(','),
          detaillist: res.data[0].fields.otherpic.split(','),
          datestr: myDate.toLocaleString(),
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/getcomment?productid=' + options.id,
      success: function (res) {
        //console.log(res.data)
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
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=4',
      success: function (res) {
        self.setData({
          'man': parseInt(res.data[0].a),
          'postfee': parseInt(res.data[0].b),
        });
      }
    })
  },
  onShow: function () {
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
  ziti: function() {
    this.setData({
      province: "",
      city: "",
      address: "线下自提",
      hiddenCity: true,
    })
  },
  choosenum: function() {
    this.setData({
      hiddenChoosed: true,
    })
  },
  chooseaddr: function() {
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
          hiddenCity: true,
        })
      }
    })
  },
  dosum: function () {
    var total = this.data.productinfo.price * this.data.count
    if (total < this.data.man && this.data.productinfo.tag != '自提专用') {
      total += this.data.postfee
    }
    this.setData({
      total: total.toFixed(2),
      orders: [{ 'productid': this.data.productinfo.pk, 'number': this.data.count }]
    })
  },
  dopay: function () {
    var self = this
    if (this.data.count < 1) {
      wx.showToast({
        title: '请选数量',
      })
      return -1
    }
    if (this.data.address == '请选择配送地址' && this.data.productinfo.tag != '自提专用') {
      wx.showToast({
        title: '请填地址',
      })
      return -1
    }
    if (this.data.count > this.data.productinfo.number) {
      wx.showToast({ title: '库存不足' })
      return -1
    }
    var total = parseFloat(this.data.total)
    var balance = parseFloat(this.data.balance)
    if (total > balance) {
      wx.request({
        url: app.globalData.apiURL + '/payable',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          memberid: wx.getStorageSync('memberid'),
          amount: total - balance,
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
  makeorder: function () {
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
        if (res.data == 'order completed') {
          wx.showModal({
            title: '下单成功',
            content: '你可在我的订单中查看或取消',
            success(res1) {
              if (res1.confirm) {
                wx.navigateTo({
                  url: '../myself/myOrder',
                })
              }
            }
          })
          self.refreshbalance()
        } else {
          wx.showModal({
            title: '下单错误',
            content: res.data,
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
  showChoosedDialog: function() {
  this.setData({
    hiddenChoosed: false
  })
  },
  showCityDialog: function() {
  this.setData({
    hiddenCity: false
  })
  },
  showServerDialog: function() {
  this.setData({
    hiddenServer: false
  })
  },
  showCouponDialog: function() {
  this.setData({
    hiddenCoupon: false
  })
  },
  addCity: function() {
  this.hideAllDialog();
  this.setData({
    hiddenAddCity: false
  })
  },
  hideAllDialog: function() {
  this.setData({
    hiddenChoosed: true,
    hiddenCity: true,
    hiddenServer: true,
    hiddenCoupon: true,
    hiddenAddCity: true
  })
  },
  tapNavEvaluate: function() {
    wx.navigateTo({
      url: './evaluate?productid='+this.data.productid
    })
  },
  tapNavHome: function () {
    wx.switchTab({
      url: '../experience/showAll',
    })
  },
  tapCreateOrder: function() {
  wx.navigateTo({
    url: './address'
  })
  },
  tapPreviewImage: function(e) {
  var urls = [];
  var url = e.target.dataset.url;
  urls.push(url);
  wx.previewImage({
    urls: urls,
  })
  },
  tapShopCart: function() {
  wx.navigateTo({
    url: '../myself/myOrder'
  })
  },
  onShareAppMessage: function () {
    return {
      title: '发现好货：' + this.data.productinfo.title,
      success: function (res) {
      wx.showToast({
        title: '谢谢分享',
      })
      }
    }
  }
})
