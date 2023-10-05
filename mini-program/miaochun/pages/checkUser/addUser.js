const app = getApp()

Page({
  data: {
    id: "",
    xm: "",
    phone: "",
    email: "",
    update: false,
  },
  addgeter: function (e) {
    var self = this
    var xm = e.detail.value.xm
    var phone = e.detail.value.phone
    var email = e.detail.value.email
    if (!xm) {wx.showToast({ title: '请完整填写姓名', duration: 1000 });return -1}
    if (!phone) {wx.showToast({ title: '请完整填写电话', duration: 1000 }); return -1}
    if (parseInt(phone)!=phone) {wx.showToast({ title: '电话需全是数字', duration: 1000 }); return -1}
    if (this.data.update) {
      var suburl = '/buyer/update'
      var data = { buyerId: this.data.id, name: xm, mobile: phone, mail: email }
    } else {
      var suburl = '/buyer/add'
      var data = { name: xm, mobile: phone, mail: email }
    }
    wx.request({
      url: app.globalData.apiURL + suburl,
      header: {
        memberId: wx.getStorageSync('memberid'),
        token: wx.getStorageSync('token'),
      },
      data: data,
      method: 'POST',
      success: function (res) {
        wx.showToast({
          title: '完成',
          icon: 'success',
          duration: 1000
        })
        wx.navigateTo({
          url: 'checkUser'
        })
      }
    })   
  },
  onLoad: function (options) {
    var self = this
    if (options.id) {
      this.setData({
        id: options.id,
        xm: options.xm,
        phone: options.phone,
        email: options.email,
        update: true,
      })
    }
    wx.setNavigationBarTitle({
      title: '编辑取票人',
    })
  }
})