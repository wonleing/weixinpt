SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
CREATE TABLE IF NOT EXISTS `__pname___1` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___1` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, '北京水蜜桃', '原价15.8元/公斤 世果汇水果,北京水蜜桃', '12.6', 'http://img14.360buyimg.com/n4/g12/M00/02/09/rBEQYFGHi6kIAAAAAAHwOacDvqIAAAchQDWoLMAAfBR666.jpg', ''),
(2, '挪威新鲜三文鱼', '原价62元/斤 鲜码头挪威新鲜三文鱼刺身冷冻生鱼片 送芥末酱油', '48', 'http://img12.360buyimg.com/n2/g5/M02/1B/14/rBEIDFAWBmcIAAAAAAK2NEN7_isAAFZZQNG6MoAArZM915.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___2` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___2` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, '费列罗四层夹心榛果巧克力', '原价208 费列罗四层夹心榛果巧克力 96粒加大装婚礼装，进口产品', '168', 'http://img12.360buyimg.com/n2/g9/M03/07/01/rBEHaVBW5u0IAAAAAAS1DZo9YowAABX-wF-sdYABLUl631.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___3` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___3` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, '海飞丝750ml装', '原价60 海飞丝去屑洗发露丝质柔滑型750ml优惠装', '48', 'http://img10.360buyimg.com/n4/g7/M03/08/1C/rBEHZlB73NAIAAAAAAD4GFoJ5ZAAABvQQK-vLAAAPgw421.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___4` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___4` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, 'NIKE篮球', '原价169 NIKE耐克GAMETACK外场篮球 BB0451801', '128', 'http://img11.360buyimg.com/n4/1396/be59775c-6788-4828-b078-54089c45fde9.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___5` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___5` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, 'DF女牛仔短裙', '原价55 DF女装牛仔短裙 女夏装热卖韩版潮磨破显瘦女牛仔短裙', '38', 'http://img13.360buyimg.com/n4/g12/M00/0A/11/rBEQYFGisAsIAAAAAAJCXcFjBs8AACDpgM_xrUAAkJ1389.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___6` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___6` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, '美的5L电压力锅', '原价339元 美的（Midea）W13PLS505E 多功能智能化电脑版 5L电压力锅', '288', 'http://img12.360buyimg.com/n2/g10/M00/08/14/rBEQWVE4ZUEIAAAAAAFlg7tdIYMAABr6QHdEHgAAWWb205.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___7` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___7` (`id`, `title`, `description`, `price`, `pic`, `link`) VALUES
(1, '汽车门把手保护膜', '原价39元 3M第二代汽车门把手保护膜 犀牛皮保护贴膜4片装', '28', 'http://img12.360buyimg.com/n2/g12/M00/0B/00/rBEQYFGkIAIIAAAAAAFftrvFTYcAACJmwCO9bAAAV_O623.jpg', '');

CREATE TABLE IF NOT EXISTS `__pname___main` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `__pname___main` (`id`, `title`, `description`, `pic`, `link`, `type`) VALUES
(1, '生鲜类', '', 'http://img1.voc.com.cn/UpLoadFile/2012/11/12/201211120931156324.jpg', '', 2),
(2, '食品类', '', 'http://pic18.nipic.com/20111130/8942479_024906015000_2.jpg', '', 2),
(3, '日用品', '', 'http://pic9.nipic.com/20100825/5461_225108833631_2.jpg', '', 2),
(4, '文体玩具', '', 'http://pic4.nipic.com/20090813/1986026_084349062_2.jpg', '', 2),
(5, '服装鞋帽', '', 'http://pic30.nipic.com/20130531/11064539_090902532000_2.jpg', '', 2),
(6, '家居家电', '', 'http://pic30.nipic.com/20130622/12933988_090700505105_2.jpg', '', 2),
(7, '其它产品', '', 'http://pic4.nipic.com/20091129/435203_103002075757_2.jpg', '', 2),
(8, '关于我们', '地址：沃尔玛大望路店，朝阳区建国路93号院万达广场B1楼(近大望路) 电话：010-59603566', 'http://ww2.sinaimg.cn/bmiddle/558fe6e3jw1e61f22h0dbj20nm0bf75y.jpg', 'http://j.map.baidu.com/1zxqk', 1),
(9, '二维码', '扫二维码，找特价商品，惊喜不断', 'http://ww2.sinaimg.cn/bmiddle/558fe6e3jw1e5p0psxhoej20by0bymxx.jpg', 'http://ww2.sinaimg.cn/bmiddle/558fe6e3jw1e5p0psxhoej20by0bymxx.jpg', 1);
