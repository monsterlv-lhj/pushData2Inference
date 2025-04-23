
DROP TABLE IF EXISTS `ashholdmonitoringdata`;
CREATE TABLE `ashholdmonitoringdata` (
  `id` int NOT NULL COMMENT '主键ID',
  `serialNum` int DEFAULT NULL COMMENT '编号',
  `ashHoldRate` float DEFAULT NULL COMMENT '持灰力',
  `date` date DEFAULT NULL COMMENT '检测日期',
  `curTime` time DEFAULT NULL COMMENT '检测时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='持灰力监测数据';

DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` int NOT NULL COMMENT '主键ID',
  `chanNum` varchar(45) NOT NULL COMMENT '通道编号',
  `suctionMode` varchar(45) NOT NULL COMMENT '吸力模式',
  `calibrCoef1` float DEFAULT NULL COMMENT '校准系数1',
  `calibrCoef2` float DEFAULT NULL COMMENT '校准系数2',
  `calibrCoef3` float DEFAULT NULL COMMENT '校准系数3',
  `calibrCoef4` float DEFAULT NULL COMMENT '校准系数4',
  `calibrCoef5` float DEFAULT NULL COMMENT '校准系数5',
  `calibrCoef6` float DEFAULT NULL COMMENT '校准系数6',
  `suctionTimes` int DEFAULT NULL COMMENT '吸力次数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='开机配置文件';

DROP TABLE IF EXISTS `monitoringdata`;
CREATE TABLE `monitoringdata` (
  `id` int NOT NULL COMMENT '主键ID',
  `serialNum` int DEFAULT NULL COMMENT '编号',
  `gray` int DEFAULT NULL COMMENT '白度',
  `graywithCrack` int DEFAULT NULL COMMENT '含裂口白度',
  `openingRate` float DEFAULT NULL COMMENT '裂口率',
  `ashshrinkageRate` float DEFAULT NULL COMMENT '缩灰率',
  `ashshrinkageRateForArea` float DEFAULT NULL COMMENT '缩灰率面积',
  `carbonlineWidth` float DEFAULT NULL COMMENT '碳线宽度',
  `carbonlineUniformity` float DEFAULT NULL COMMENT '碳线整齐度',
  `burningRate` float DEFAULT NULL COMMENT '燃烧速率',
  `burningStatus` varchar(45) DEFAULT NULL COMMENT '燃烧状态',
  `suctiontimes` int DEFAULT NULL COMMENT '吸力次数',
  `productBrand` varchar(45) DEFAULT NULL COMMENT '产品品牌',
  `detectTime` time DEFAULT NULL COMMENT '检测时间',
  `detectDate` date DEFAULT NULL COMMENT '检测日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='记录烟支燃烧时的各项指标数据。';

DROP TABLE IF EXISTS `monitoringrecorde`;
CREATE TABLE `monitoringrecorde` (
  `id` int NOT NULL COMMENT '主键ID',
  `detectTime` date DEFAULT NULL COMMENT '检测日期',
  `detectPerson` varchar(45) DEFAULT NULL COMMENT '检测人',
  `brand` varchar(45) DEFAULT NULL COMMENT '品牌',
  `detectType` varchar(45) DEFAULT NULL COMMENT '检测类型',
  `cigLength` int DEFAULT NULL COMMENT '烟支长度',
  `burningLength` int DEFAULT NULL COMMENT '燃烧长度',
  `burningType` varchar(45) DEFAULT NULL COMMENT '燃烧类型',
  `suctionModel` varchar(45) DEFAULT NULL COMMENT '吸力模式',
  `shootModel` varchar(45) DEFAULT NULL COMMENT '拍照模式',
  `curDetectTime` time DEFAULT NULL COMMENT '当前检测时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='燃烧监测记录';

DROP TABLE IF EXISTS `polycurvedata`;
CREATE TABLE `polycurvedata` (
  `id` int NOT NULL COMMENT '主键ID',
  `date` date DEFAULT NULL COMMENT '日期',
  `productBrand` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '品牌',
  `groupNum` int DEFAULT NULL COMMENT '分组号',
  `channelNum` int DEFAULT NULL COMMENT '通道号',
  `scanNum` int DEFAULT NULL COMMENT '扫描编号',
  `fireLength` double DEFAULT NULL COMMENT '灰柱长度',
  `carbonLineWidth` double DEFAULT NULL COMMENT '碳线宽度',
  `carbonLineUniformity` double DEFAULT NULL COMMENT '碳线整齐度',
  `burningRate` double DEFAULT NULL COMMENT '燃烧速率',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin COMMENT='多组曲线数据';

DROP TABLE IF EXISTS `sysparaset`;
CREATE TABLE `sysparaset` (
  `burningModel` int NOT NULL COMMENT '燃烧模式编号',
  `cigarLength` int DEFAULT NULL COMMENT '烟支长度',
  `suctionPara` int DEFAULT NULL COMMENT '吸力参数',
  `suctionCapcity` int DEFAULT NULL COMMENT '吸力容量',
  `suctionInerval` int DEFAULT NULL COMMENT '吸力间隔',
  `suctionContinus` int DEFAULT NULL COMMENT '持续吸力',
  `rotateAngle` int DEFAULT NULL COMMENT '旋转角度',
  `swingTime` float DEFAULT NULL COMMENT '摆动时间',
  `rotatecycle` float DEFAULT NULL COMMENT '旋转周期',
  `rotateTime` float DEFAULT NULL COMMENT '旋转时间',
  PRIMARY KEY (`burningModel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='系统参数设置';
