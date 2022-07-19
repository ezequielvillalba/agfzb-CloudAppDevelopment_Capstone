/**
 * Get all dealerships
 */
if (require.main === module) {
    var params = {
        COUCH_URL: process.env.COUCH_URL,
        IAM_API_KEY: process.env.IAM_API_KEY,
        COUCH_USERNAME: process.env.COUCH_USERNAME,
        // st: "CA",
        sty: null,
        dealerId: 2,
    };

    main(params);
}

var keys_to_keep = ['id','city','state','st','address','zip','lat','long','short_name','full_name']

function main(params) {
    // console.log(params);
        return new Promise(function (resolve, reject) {
            const { CloudantV1 } = require('@ibm-cloud/cloudant');
            const { IamAuthenticator } = require('ibm-cloud-sdk-core');
            const authenticator = new IamAuthenticator({ apikey: "IukMHXbwqVIr_OEbs5xGIiXBiTYwdg2lVOodqpjzVLHn" })
            const cloudant = CloudantV1.newInstance({
                authenticator: authenticator
            });
            cloudant.setServiceUrl("https://c1814c9d-49ff-488e-8be9-21eaa9214c7c-bluemix.cloudantnosqldb.appdomain.cloud");
            if (params.st || params.state) {
                // return dealership with this state 
                if (params.st) { 
                    cloudant.postFind({db:'dealerships',selector:{st:params.st}})
                    .then((result)=>{
                    // console.log(result.result.docs);
                    let code = 200;
                    message = "Success"
                    if (result.result.docs.length == 0) {
                        code = 404;
                        message = "The state does not exist"
                    }
                    else {
                        redux(result.result.docs)
                    }
                    resolve({
                        statusCode: code,
                        message: message,
                        headers: { 'Content-Type': 'application/json' },
                        body: result.result.docs
                    });
                    }).catch((err)=>{
                    reject(err);
                    })
                }
                else { 
                    cloudant.postFind({db:'dealerships',selector:{st:params.state}})
                    .then((result)=>{
                    // console.log(result.result.docs);
                    let code = 200;
                    message = "Success"
                    if (result.result.docs.length == 0) {
                        code = 404;
                        message = "The state does not exist"
                    }
                    else {
                        redux(result.result.docs)
                    }
                    resolve({
                        statusCode: code,
                        message: message,
                        headers: { 'Content-Type': 'application/json' },
                        body: result.result.docs
                    });
                    }).catch((err)=>{
                    reject(err);
                    })
                }
            } else if (params.id || params.dealerId) {
                if (params.id) {
                    id = parseInt(params.id)
                    // return dealership with this state 
                    cloudant.postFind({
                    db: 'dealerships',
                    selector: {
                        id: id
                    }
                    })
                    .then((result)=>{
                    // console.log(result.result.docs);
                    let code = 200;
                    message = "Success"
                    if (result.result.docs.length == 0) {
                        code = 404;
                        message = "The id does not exist"
                        }
                        else {
                        redux(result.result.docs)
                        }
                    resolve({
                        statusCode: code,
                        message: message,
                        headers: { 'Content-Type': 'application/json' },
                        body: result.result.docs
                    });
                    }).catch((err)=>{
                    reject(err);
                    })
                } else {
                    id = parseInt(params.dealerId)
                    // return dealership with this state 
                    cloudant.postFind({
                    db: 'dealerships',
                    selector: {
                        id: id
                    }
                    })
                    .then((result)=>{
                    // console.log(result.result.docs);
                    let code = 200;
                    message = "Success"
                    if (result.result.docs.length == 0) {
                        code = 404;
                        message = "The id does not exist"
                        }
                        else {
                        redux(result.result.docs)
                        }
                    resolve({
                        statusCode: code,
                        message: message,
                        headers: { 'Content-Type': 'application/json' },
                        body: result.result.docs
                    });
                    }).catch((err)=>{
                    reject(err);
                    })
                }
                
            } else {
                // return all documents 
                cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })            
                .then((result)=>{
                  console.log(result.result.rows);
                  let code = 200;
                  message = "Success"
                  if (result.result.rows.length == 0) {
                      code = 404;
                    }
                    else {
                      var data = redux2(result.result.rows)
                    }
                  resolve({
                      statusCode: code,
                      message: message,
                      headers: { 'Content-Type': 'application/json' },
                      body: data
                  });
                }).catch((err)=>{
                  reject(err);
                })
            }
        }
    )
}
    
function redux(data) {
    data.forEach((item) => {
        Object.keys(item).forEach((key) => {
            if (!keys_to_keep.includes(key)) {
                delete (item[key])
            }
        })
    })
    console.log(data)
}

function redux2(data) {

    data.forEach((item) => {
        Object.keys(item.doc).forEach((key) => {
            if (!keys_to_keep.includes(key)) {
                delete (item.doc[key])
            }
        })
    })
    console.log(data)
    var dict = []
    for (var i in data) {
        dict.push(data[i].doc);
    }
    console.log(dict)
    return dict;
}