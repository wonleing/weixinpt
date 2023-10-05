var app = getApp()
Page({
  data: {
    orders: [],
    currentTab: 0,
    count: 20,
    currentpage: 1,
    perpage: 20,
    nomore: false,
    kdinfo: '',
    flag: true,
  },
  onShow: function () {
    const self = this;
    wx.request({
      url: app.globalData.apiURL + '/orderlist?pn=0&pp='+this.data.perpage,
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        pn: 0,
        pp: this.data.perpage,
      },
      method: 'POST',
      success: function (res) {
        //console.log(res.data)
        self.setData({
          orders: res.data,
          count: res.data.length
        })
      }
    })
    wx.setNavigationBarTitle({
      title: '我的订单'
    })
  },
  hide: function () {
    this.setData({ flag: true })
  },
  checkkd: function (e) {
    if (this.data.kdinfo != '') {
      this.setData({
        flag: false,
      })
    } else {
      var self = this
      wx.request({
        url: app.globalData.apiURL + '/forward?oid=' + e.currentTarget.id,
        success: function (res) {
          //console.log(res.data.data)
          self.setData({
            kdinfo: res.data.data,
            flag: false,
          })
        }
      })
    }
  },
  delorder: function (e) {
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/delorder',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        oid: e.currentTarget.id,
      },
      method: 'POST',
      success: function (res) {
        self.onShow()
      }
    })
  },
  buyagain: function (e) {
    wx.navigateTo({
      url: '../detail/cityDetail?id='+e.currentTarget.id
    })
  },
  /** 
     * 滑动切换tab 
     */
  bindChange: function (e) {
    var that = this;
    that.setData({ currentTab: e.detail.current });
  },
  /** 
   * 点击tab切换 
   */
  swichNav: function (e) {
    var that = this;
    if (this.data.currentTab === e.target.dataset.current) {
      return false;
    } else {
      that.setData({
        currentTab: e.target.dataset.current
      })
    }
  },
  onReachBottom: function () {
    var contents = this.data.orders
    var pn = this.data.currentpage
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/orderlist',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        pn: pn,
        pp: this.data.perpage,
      },
      method: 'POST',
      success: function (res) {
        if (res.data.length > 0) {
          contents = contents.concat(res.data)
          pn += 1
        } else {
          self.setData({
            nomore: true
          });
        }
        self.setData({
          orders: contents,
          currentpage: pn,
        });
      }
    })
  }
})
