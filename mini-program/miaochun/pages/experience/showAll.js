const app = getApp()
Page({
  data: {
    goods: [],
  },
  onLoad: function (option) {
    const self = this
    var goods = []
    wx.setNavigationBarTitle({
      title: '妙纯乳品店',
    })
    if (option.memberid) {
      wx.setStorageSync('memberid', option.memberid)
    }
    wx.request({
      url: app.globalData.apiURL + '/getsetting?type=1',
      success: function (res) {
        self.setData({
          banner: res.data
        });
      }
    })
    wx.request({
      url: app.globalData.apiURL + '/productlist?onsale=1',
      success: function (res) {
        for (var i=0;i<res.data.length;i++) {
          goods[i] = { 'id': res.data[i].pk, 'title': res.data[i].fields.title, 'price': res.data[i].fields.price, 'tag': res.data[i].fields.tag, 'pic': res.data[i].fields.pic.split(",")[0], 'des': res.data[i].fields.description}
        }
        self.setData({
          goods: goods
        });
      }
    })
  },
  enterdetail: function (event) {
    wx.navigateTo({
      url: '../goods/index?id=' + event.currentTarget.id
    })
  },
  onShareAppMessage: function () {
    return {
      title: '妙纯乳品店',
      success: function (res) {
        wx.showToast({
          title: '谢谢分享',
        })
      }
    }
  }
  // onReachBottom: function () {
  //   this.setData({
  //     isLoading: true
  //   })
  //   var contents = this.data.shops
  //   var pn = this.data.currentpage
  //   const self = this
  //   wx.request({
  //     url: app.globalData.apiURL + '/memberlist?pn=' + pn + '&pp=' + this.data.perpage,
  //     success: function (res) {
  //       if (res.data.length > 0) {
  //         contents = contents.concat(res.data)
  //         pn += 1
  //       } else {
  //         self.setData({
  //           nomore: true
  //         });
  //       }
  //       self.setData({
  //         shops: contents,
  //         currentpage: pn,
  //         isLoading: false
  //       });
  //     }
  //   })
  // }
})
