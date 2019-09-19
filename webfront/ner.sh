# 鈴木さんがきょうの9時30分に横浜に行きます。
curl -i -X POST -H "Content-Type:application/json" -d '{ "request_id":"record001", "sentence":"Mr. Suzuki goes to New York City today."}' 'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/entity?APIKEY=43466571565539376663774f43734d2f68544b4c48463069343232306f6131434a6c4a41434e694157582f'
