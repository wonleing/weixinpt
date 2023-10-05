const app = getApp()
Page({
  data: {
    comments: [],
    productid: '',
  },
  onLoad: function(option) {
    var self = this
    wx.request({
      url: app.globalData.apiURL + '/getcomment?productid=' + option.productid,
      success: function (res) {
        self.setData({
          productid: option.productid,
          comments: res.data,
        })
      }
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
          productid: this.data.productid,
          content: e.detail.value.content,
        },
        method: 'POST',
        success: function (res) {
          wx.showToast({
            title: '评论成功',
          })
          wx.navigateBack({
            delta: 1
          })
        }
      })
    }
  },
  tapPreviewImage: function(e) {
    var urls = [e.target.dataset.url];
    wx.previewImage({
      urls: urls,
    })
  }
})
