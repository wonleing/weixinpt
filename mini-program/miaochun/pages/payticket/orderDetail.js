const app = getApp()
Page({
  data: {
    total: 0,
    discount: [],
  },
  dopay: function (f) {
    var amount = f.detail.value.amount
    if (f.detail.value.otheramount) {
      amount = f.detail.value.otheramount
    }
    wx.request({
      url: app.globalData.apiURL + '/payable',
      data: { userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        memberid: wx.getStorageSync('memberid'),
        amount:amount },
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
            wx.showModal({
              title: '充值成功',
              content: '接下来可以下单发货了',
              success: function (res) {
                if (res.confirm) {
                  wx.switchTab({url: '../experience/showAll',})
                }
              }
            })
          },
          'fail': function (res2) {
            wx.showToast({ title: '支付取消', })
            //wx.switchTab({ url: '../experience/showAll', })
          }
        })
      },
    })
  },
  onLoad: function (option) {
    if (option.memberid) {
      wx.setStorageSync('memberid', option.memberid)
    }
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=2',
      success: function (res) {
        self.setData({
          discount: res.data,
        })
      }
    })
    wx.setNavigationBarTitle({
      title: '优惠充值'
    })
  }
})
