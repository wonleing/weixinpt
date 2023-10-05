const app = getApp()
Page({
  data: {
    indicatorDots: true,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    productinfo:{},
    productid: '',
    count: 0,
    total: 0,
    address: '',
    isCollect: '',
    videoURL: '',
  },
  onLoad: function (options) {
    wx.setNavigationBarTitle({
      title: '产品详情'
    })
    const self = this
    const pid = options.id;
    wx.request({
      url: app.globalData.apiURL + '/productlist?productid='+pid,
      success: function (res) {
        var morepic = res.data[0].fields.otherpic
        if (morepic.endsWith(".mp4")) {
          self.setData({ videoURL: morepic })
        }
        self.setData({
          productinfo: res.data[0],
          productid: pid,
          slidelist: morepic.split(','),
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/colproduct',
      method: 'POST',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        productid: pid,
        action: 'query'
      },
      success: function (res) {
        self.setData({
          isCollect: res.data
        })
      }
    })
  },
  selectaddr: function () {
    var self=this
    wx.chooseAddress({
      success: function (res) {
        self.setData({
          address: res.provinceName + res.cityName + res.countyName + res.detailInfo + '\n' + res.userName + res.telNumber
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
    wx.request({
      url: app.globalData.apiURL + '/payable',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        orders: this.data.orders,
        address: e.detail.value.address,
        goodname: this.data.productinfo.fields.title,
      },
      method: 'POST',
      success: function (res1) {
        //console.log(res1.data)
        wx.requestPayment({
          'timeStamp': res1.data.timeStamp,
          'nonceStr': res1.data.nonceStr,
          'package': res1.data.package,
          'signType': res1.data.signType,
          'paySign': res1.data.paySign,
          'success': function (res2) {
            wx.showToast({ title: '购买成功' })
          },
          'fail': function (res2) {
            console.log(res2)
            wx.showToast({ title: '支付取消' })
          }
        })
      }
    })
  },
  optCollect: function () {
    var self = this
    if (this.data.isCollect == 'True') {
      wx.request({
        url: app.globalData.apiURL + '/colproduct',
        method: 'POST',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          productid: this.data.productid,
          action: 'del'
        },
        success: function (res) {
          wx.showToast({ title: '取消成功' })
          self.setData({ isCollect: 'False' })
        },
        fail: function (res) { console.log(res) }
      })
    } else {
      wx.request({
        url: app.globalData.apiURL + '/colproduct',
        method: 'POST',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          productid: this.data.productid,
          action: 'add',
        },
        success: function (res) {
          wx.showToast({ title: '收藏成功' })
          self.setData({ isCollect: 'True' })
        },
        fail: function (res) { console.log(res) }
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