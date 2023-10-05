const app = getApp()

Page({
  data: {
    indicatorDots: true,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    showpay: false,
    showCostExplain: false,
    showmore: false,
    textofmore: '查看更多',
    isCollect: '',
    memberid: '',
    memberinfo: {},
    productlist: [],
    memberdescription: "",
    slidelist: [],
    videoURL: '',
  },
  productdetail: function (e) {
    wx.navigateTo({
      url: '../detail/cityDetail?id=' + e.currentTarget.id
    })
  },
  gotomall: function () {
    wx.switchTab({
      url: '../experience/enterSubject',
    })
  },
  callPhone: function (e) {
    var phoneNumber = e.currentTarget.dataset.phonenumber;
    wx.makePhoneCall({
      phoneNumber: phoneNumber,
      success: function () {
        console.log("拨打电话"+phoneNumber)
      },
      fail: function () {
        console.log("拨打电话失败！")
      }
    })
  },
  ScreenImg: function (e) {
    var imgUrl = e.currentTarget.dataset.imgurl;
    var imgs = [];
    imgs.push(imgUrl);
    wx.previewImage({
      urls: imgs // 需要预览的图片http链接列表
    })
  },
  optCollect: function () {
    var self = this
    if (this.data.isCollect=='True') {
      wx.request({
        url: app.globalData.apiURL + '/colmember',
        method: 'POST',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          memberid: this.data.memberid,
          action: 'del'
        },
        success: function (res) {
          wx.showToast({title: '取消成功'})
          self.setData({ isCollect: 'False' })
        },
        fail: function (res) {console.log(res)}
      })
    } else {
      wx.request({
        url: app.globalData.apiURL + '/colmember',
        method: 'POST',
        data: {
          userid: wx.getStorageSync('userid'),
          token: wx.getStorageSync('token'),
          memberid: this.data.memberid,
          action: 'add',
        },
        success: function (res) {
          wx.showToast({ title: '收藏成功' })
          self.setData({isCollect: 'True'})
        },
        fail: function (res) { console.log(res) }
      })
    }
  },
  showCostexplain: function () {
    this.setData({ showCostExplain: !this.data.showCostExplain });
  },
  hideDialog: function () {
    this.setData({ showCostExplain: false });
  },
  showDialog: function () {
    this.setData({ showCostExplain: true });
  },
  goorder: function (e) {
    wx.navigateTo({
      url: '../payticket/orderDetail?shopid=' + e.currentTarget.id
    })
  },
  viewdetail: function(event) {
    wx.navigateTo({
      url: 'viewDetail?id=' + event.currentTarget.id
    })
  },
  activeDetail: function (e) {
    wx.navigateTo({
      url: '../experience/activeDetail?shopId=' + e.currentTarget.id
    })
  },
  onLoad: function (option) {
    var self = this
    var memberid = option.id
    wx.setNavigationBarTitle({
      title: '展商详情'
    })
    wx.request({
      url: app.globalData.apiURL + '/memberdetail?memberid=' + memberid,
      success: function (res) {
        var morepic = res.data[0].fields.otherpic
        if (morepic.endsWith(".mp4")) {
          self.setData({videoURL: morepic})
        }
        self.setData({
          memberinfo: res.data[0],
          memberid: memberid,
          lat: res.data[0].fields.lat,
          lon: res.data[0].fields.lon,
          memberdescription: res.data[0].fields.detail.replace(/=/g, '\n'),
          slidelist: morepic.split(","),
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/productlist?memberid=' + memberid,
      success: function (res) {
        self.setData({
          productlist: res.data,
        })
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/colmember',
      method: 'POST',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        memberid: memberid,
        action: 'query'
      },
      success: function (res) {
        self.setData({
          isCollect: res.data
        })
      }
    })
  }, 
  onReachBottom: function () {
      this.setData({showpay: true});
  },
  checkMore: function () {
    if (this.data.textofmore == '查看更多') {
      this.setData({
        showmore: true,
        textofmore: '收起'
      });
    } else {
      this.setData({
        showmore: false,
        textofmore: '查看更多'
      });
    }
  },
  onPageScroll: function () {
    this.setData({
      showpay: true
    })
  },
  touchMove: function () {
    this.setData({
      showpay: true
    })
  },
  gotolocation: function () {
    wx.openLocation({
      latitude: this.data.lat,
      longitude: this.data.lon,
      name: this.data.memberinfo.fields.name,
      scale: 17,
    })
  },
})
