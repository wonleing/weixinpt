const app = getApp()
Page({
  data: {
    shops: [],
    currentpage: 1,
    perpage: 20,
    isLoading: false,
    nomore: false,
  },
  onLoad: function (option) {
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/colmemberlist',
      method: 'POST',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        pn: 0,
        pp: this.data.perpage,
      },
      success: function (res) {
        //console.log(res.data)
        self.setData({
          shops: res.data,
        });
      }
    })
    wx.setNavigationBarTitle({
      title: '收藏展商'
    })
  },
  enterdetail: function (event) {
    wx.navigateTo({
      url: '../detail/viewDetail?id=' + event.currentTarget.id
    })
  },
  onReachBottom: function () {
    this.setData({
      isLoading: true
    })
    var contents = this.data.shops
    var pn = this.data.currentpage
    const self = this
    wx.request({
      url: app.globalData.apiURL + '/colmemberlist',
      method: 'POST',
      data: {
        userid: wx.getStorageSync('userid'),
        token: wx.getStorageSync('token'),
        pn: pn,
        pp: this.data.perpage,
      },
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
          shops: contents,
          currentpage: pn,
          isLoading: false
        });
      }
    })
  }
})