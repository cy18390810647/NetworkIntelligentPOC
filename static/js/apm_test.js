//散点图请求数据模版
var REQUEST_SCATTER_DATA_TPL = {
	"query": {
		"bool": {
			"must": [{
				"multi_match": {
					"query": "LOMS-AUTH-22",
					"type": "phrase",
					"slop": 0,
					"fields": ["agentId"]

				}
			}],
			"filter": {
				"range": {
					"startTime": {
						"gte": 1560221660852,
						"lte": 1560221660852
					}
				}
			}
		}
	},
	"_source": [
		"startTime",
		"exceptionId",
		"errCode",
		"agentId",
		"elapsed",
		"transactionId.transactionSequence"
	],
	"size": 1
};

//散点图返回数据模版
var RESPONSE_SCATTER_DATA_TPL = {
	"currentServerTime": 1560143389177,
	"resultFrom": 1559971347518,
	"resultTo": 1560142985429,
	"scatter": {
		"metadata": {
			"1": ["LOMS-ORDER-WEB-22", "LOMS-ORDER-WEB-22", 1559829477041]
		},
		"dotList": [ // 参考 ~/pinpoint/web/src/main/java/com/navercorp/pinpoint/web/view/ScatterDataSerializer.java
			[172397429, 366, 1, 206, 1, 1], //acceptedTime,elapsedTime,agentId,transactionId.sequence,simpleExceptionCode,thick
			[167966308, 224, 1, 205, 1, 1],
		]
	},
	"from": 1559970588000, //对应x轴坐标0点
	"to": 1560143388000,
	"complete": true
};

//克隆方法
var clone = function(data) {
	return JSON.parse(JSON.stringify(data))
};

/**
 * @description 调用ajax
 */
function ajaxCall(path, data, callback) {
	$.ajax({
		headers: {
			"content-type": "text/html; charset=UTF-8",
			//"kbn-xpack-sig": "5899560a41e80e8aa157d3c6f4bda6ed",
			//"Transfer-Encoding": "chunked",
		},
		type: "POST",
		dataType: "JSON",
		data: data,
		crossDomain: true,
		url: "http://192.168.1.152:5601/app/kibana",
		success: function(res) {
			console.info(res);
			callback(res);
		},
		error: function(error) {
			console.error(error);
		}
	})
}

/**
 * @description: 根据探针ID获取该探针ID上所有请求的散点图
 * @callback: 异步调用返回的回调函数
 * @agentId: agentId,对应app
 * @from: 开始时间戳，毫秒为单位
 * @to: 结束时间戳，毫秒为单位
 * @limit: 返回记录数上限
 * @xGroupUnit: x轴数值1代表的毫秒数
 * @yGroupUnit: y轴数值1代表的毫秒数
 * @return: 参考 RESPONSE_SCATTER_DATA_TPL 数据结构
 */

function getScatterDataByAgentId(callback, agentId, from, to, limit, xGroupUnit, yGroupUnit) {
	var data = clone(REQUEST_SCATTER_DATA_TPL);
	data.query.bool.must[0].multi_match.query = agentId;
	data.query.bool.must[0].multi_match.fields = ["agentId"];
	data.query.bool.filter.range.startTime.gte = from;
	data.query.bool.filter.range.startTime.lte = to;
	data.size = limit;
	var myCallback = function(data) {
		var source = data.hits.hits;
		var result = clone(RESPONSE_SCATTER_DATA_TPL);
		result.from = from;
		result.to = to;
		result.currentServerTime = new Date().getTime();
		result.complete = (data.hits.hits.length == data.hits.total);
		result.resultFrom = to;
		result.resultTo = from;
		result.scatter.dotList = [];
		source.forEach(function(item) {
			item = item._source;
			if (result.resultFrom > item.startTime) {
				result.resultFrom = item.startTime;
			}
			if (result.resultTo < item.startTime) {
				result.resultTo = item.startTime;
			}
			var arr = [];
			arr.push(item.startTime - from);
			arr.push(item.elapsed);
			arr.push(0); //TODO: 此处存疑
			arr.push(item.transactionId.transactionSequence);
			arr.push(item.exceptionId); //TODO: 此处存疑
			arr.push(0); //TODO: 此处存疑
			result.scatter.dotList.push(arr);
			result.scatter.metadata["1"][0] = item.agentId; //TODO: 此处存疑
			result.scatter.metadata["1"][1] = item.agentId; //TODO: 此处存疑
			result.scatter.metadata["1"][2] = item.startTime; //TODO: 此处存疑
		})
		callback(data);
	};
	ajaxCall("/tracev2span-*/_search", JSON.stringify(data), myCallback);
}

function getScatterDataBySQLLink(callback, sqlLink, from, to, limit, xGroupUnit, yGroupUnit) {
	ajaxCall("/tracev2span-*/_search", "{}", callback)
}

function getScatterDataByNOSQLLink(callback, nosqlLink, from, to, limit, xGroupUnit, yGroupUnit) {
	ajaxCall("/tracev2span-*/_search", "{}", callback)
}

/**
 * @description: 根据探针Domain获取所有请求的散点图
 * @callback: 异步调用返回的回调函数
 * @agentId: agentId,对应app
 * @from: 开始时间戳，毫秒为单位
 * @to: 结束时间戳，毫秒为单位
 * @limit: 返回记录数上限
 * @xGroupUnit: x轴数值1代表的毫秒数
 * @yGroupUnit: y轴数值1代表的毫秒数
 * @return: 参考 RESPONSE_SCATTER_DATA_TPL 数据结构
 */
function getScatterDataByDomain(callback, domain, from, to, limit, xGroupUnit, yGroupUnit) {
	//根据domain获取agentId
	var data = {
		"query": {}
	};
	/*var data = {
		"query": {
			"bool": {
				"should": [{
					"multi_match": {
						"query": "192.168.1.152",
						"type": "phrase",
						"slop": 0,
						"fields": ["hostName"]

					}
				}, {
					"multi_match": {
						"query": "192.168.1.152",
						"type": "phrase",
						"slop": 0,
						"fields": ["ip"]

					}
				}]
			}
		},
		"_source": ["hostName","ip","ports","applicationName","serviceTypeCode"],
		"size":100
};*/
	var myCallback = function(data){
		console.log(data);
	};
	console.log("111",JSON.stringify(data));
	ajaxCall("/agentinfo-*/_search", JSON.stringify(data), myCallback)
}
