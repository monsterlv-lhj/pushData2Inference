
DROP TABLE IF EXISTS `ashholdmonitoringdata`;
CREATE TABLE `ashholdmonitoringdata` (
  `id` int NOT NULL COMMENT '����ID',
  `serialNum` int DEFAULT NULL COMMENT '���',
  `ashHoldRate` float DEFAULT NULL COMMENT '�ֻ���',
  `date` date DEFAULT NULL COMMENT '�������',
  `curTime` time DEFAULT NULL COMMENT '���ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='�ֻ����������';

DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` int NOT NULL COMMENT '����ID',
  `chanNum` varchar(45) NOT NULL COMMENT 'ͨ�����',
  `suctionMode` varchar(45) NOT NULL COMMENT '����ģʽ',
  `calibrCoef1` float DEFAULT NULL COMMENT 'У׼ϵ��1',
  `calibrCoef2` float DEFAULT NULL COMMENT 'У׼ϵ��2',
  `calibrCoef3` float DEFAULT NULL COMMENT 'У׼ϵ��3',
  `calibrCoef4` float DEFAULT NULL COMMENT 'У׼ϵ��4',
  `calibrCoef5` float DEFAULT NULL COMMENT 'У׼ϵ��5',
  `calibrCoef6` float DEFAULT NULL COMMENT 'У׼ϵ��6',
  `suctionTimes` int DEFAULT NULL COMMENT '��������',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='���������ļ�';

DROP TABLE IF EXISTS `monitoringdata`;
CREATE TABLE `monitoringdata` (
  `id` int NOT NULL COMMENT '����ID',
  `serialNum` int DEFAULT NULL COMMENT '���',
  `gray` int DEFAULT NULL COMMENT '�׶�',
  `graywithCrack` int DEFAULT NULL COMMENT '���ѿڰ׶�',
  `openingRate` float DEFAULT NULL COMMENT '�ѿ���',
  `ashshrinkageRate` float DEFAULT NULL COMMENT '������',
  `ashshrinkageRateForArea` float DEFAULT NULL COMMENT '���������',
  `carbonlineWidth` float DEFAULT NULL COMMENT '̼�߿��',
  `carbonlineUniformity` float DEFAULT NULL COMMENT '̼�������',
  `burningRate` float DEFAULT NULL COMMENT 'ȼ������',
  `burningStatus` varchar(45) DEFAULT NULL COMMENT 'ȼ��״̬',
  `suctiontimes` int DEFAULT NULL COMMENT '��������',
  `productBrand` varchar(45) DEFAULT NULL COMMENT '��ƷƷ��',
  `detectTime` time DEFAULT NULL COMMENT '���ʱ��',
  `detectDate` date DEFAULT NULL COMMENT '�������',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='��¼��֧ȼ��ʱ�ĸ���ָ�����ݡ�';

DROP TABLE IF EXISTS `monitoringrecorde`;
CREATE TABLE `monitoringrecorde` (
  `id` int NOT NULL COMMENT '����ID',
  `detectTime` date DEFAULT NULL COMMENT '�������',
  `detectPerson` varchar(45) DEFAULT NULL COMMENT '�����',
  `brand` varchar(45) DEFAULT NULL COMMENT 'Ʒ��',
  `detectType` varchar(45) DEFAULT NULL COMMENT '�������',
  `cigLength` int DEFAULT NULL COMMENT '��֧����',
  `burningLength` int DEFAULT NULL COMMENT 'ȼ�ճ���',
  `burningType` varchar(45) DEFAULT NULL COMMENT 'ȼ������',
  `suctionModel` varchar(45) DEFAULT NULL COMMENT '����ģʽ',
  `shootModel` varchar(45) DEFAULT NULL COMMENT '����ģʽ',
  `curDetectTime` time DEFAULT NULL COMMENT '��ǰ���ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='ȼ�ռ���¼';

DROP TABLE IF EXISTS `polycurvedata`;
CREATE TABLE `polycurvedata` (
  `id` int NOT NULL COMMENT '����ID',
  `date` date DEFAULT NULL COMMENT '����',
  `productBrand` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'Ʒ��',
  `groupNum` int DEFAULT NULL COMMENT '�����',
  `channelNum` int DEFAULT NULL COMMENT 'ͨ����',
  `scanNum` int DEFAULT NULL COMMENT 'ɨ����',
  `fireLength` double DEFAULT NULL COMMENT '��������',
  `carbonLineWidth` double DEFAULT NULL COMMENT '̼�߿��',
  `carbonLineUniformity` double DEFAULT NULL COMMENT '̼�������',
  `burningRate` double DEFAULT NULL COMMENT 'ȼ������',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin COMMENT='������������';

DROP TABLE IF EXISTS `sysparaset`;
CREATE TABLE `sysparaset` (
  `burningModel` int NOT NULL COMMENT 'ȼ��ģʽ���',
  `cigarLength` int DEFAULT NULL COMMENT '��֧����',
  `suctionPara` int DEFAULT NULL COMMENT '��������',
  `suctionCapcity` int DEFAULT NULL COMMENT '��������',
  `suctionInerval` int DEFAULT NULL COMMENT '�������',
  `suctionContinus` int DEFAULT NULL COMMENT '��������',
  `rotateAngle` int DEFAULT NULL COMMENT '��ת�Ƕ�',
  `swingTime` float DEFAULT NULL COMMENT '�ڶ�ʱ��',
  `rotatecycle` float DEFAULT NULL COMMENT '��ת����',
  `rotateTime` float DEFAULT NULL COMMENT '��תʱ��',
  PRIMARY KEY (`burningModel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='ϵͳ��������';
