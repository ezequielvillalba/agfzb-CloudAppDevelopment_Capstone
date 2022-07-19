/**
 * Get all dealerships
 */

 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 
if (require.main === module) {
    var params = {
        COUCH_URL: process.env.COUCH_URL,
        IAM_API_KEY: process.env.IAM_API_KEY,
        COUCH_USERNAME: process.env.COUCH_USERNAME,
        st: "CA",
        id: null,
    };

    main(params);
}
 
 function main(params) {
    const authenticator = new IamAuthenticator({ apikey: "IukMHXbwqVIr_OEbs5xGIiXBiTYwdg2lVOodqpjzVLHn" })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl("https://c1814c9d-49ff-488e-8be9-21eaa9214c7c-bluemix.cloudantnosqldb.appdomain.cloud");
 
   
    dbs = getDBs(cloudant);
    console.log(dbs)
    // return dbs

    response = getMatchingRecords(cloudant, 'dealerships', {st:params.st})
    console.log(response)
    return response
//    console.log(response)

//    console.log(response)
 }

/*
Implementation to get all databases names
*/
async function getDBs(cloudant) {
    try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
    } catch (error) {
        return { error: error.description };
    }
}

/*
Implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
*/

var keys_to_keep = ['id','city','state','st','address','zip','lat','long']
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
async function getMatchingRecords(cloudant,dbname, selector) {

    try {
        let data = await cloudant.postFind({db:dbname,selector:selector})
        redux (data.result.docs);
        return { result:data.result.docs };
    } catch (error) {
        return { error: error.description };
    }
}


 

// function main(params) {
//     // console.log(params);
//     return new Promise(function (resolve, reject) {
//         const { CloudantV1 } = require('@ibm-cloud/cloudant');
//         const { IamAuthenticator } = require('ibm-cloud-sdk-core');
//         const authenticator = new IamAuthenticator({ apikey: 'xzal2JkyNbbdidgTQJzePu85rN0266G4DXuYiTxQ5jo2' })
//         const cloudant = CloudantV1.newInstance({
//             authenticator: authenticator
//         });
//         cloudant.setServiceUrl('https://f093dd17-242b-4f82-bb6e-aaef08d3d338-bluemix.cloudantnosqldb.appdomain.cloud');
//         if (params.st) {
//             // return dealership with this state 
//             cloudant.postFind({db:'dealerships',selector:{st:params.st}})
//             .then((result)=>{
//               // console.log(result.result.docs);
//               let code = 200;
//               if (result.result.docs.length == 0) {
//                   code = 404;
//               }
//               resolve({
//                   statusCode: code,
//                   headers: { 'Content-Type': 'application/json' },
//                   body: result.result.docs
//               });
//             }).catch((err)=>{
//               reject(err);
//             })
//         } else if (params.id) {
//             id = parseInt(params.dealerId)
//             // return dealership with this state 
//             cloudant.postFind({
//               db: 'dealerships',
//               selector: {
//                 id: parseInt(params.id)
//               }
//             })
//             .then((result)=>{
//               // console.log(result.result.docs);
//               let code = 200;
//               if (result.result.docs.length == 0) {
//                   code = 404;
//               }
//               resolve({
//                   statusCode: code,
//                   headers: { 'Content-Type': 'application/json' },
//                   body: result.result.docs
//               });
//             }).catch((err)=>{
//               reject(err);
//             })
//         } else {
//             // return all documents 
//             cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })            
//             .then((result)=>{
//               // console.log(result.result.rows);
//               let code = 200;
//               if (result.result.rows.length == 0) {
//                   code = 404;
//               }
//               resolve({
//                   statusCode: code,
//                   headers: { 'Content-Type': 'application/json' },
//                   body: result.result.rows
//               });
//             }).catch((err)=>{
//               reject(err);
//             })
//       }
//     }
//     )}


// function getDbs(cloudant) {
//     return new Promise((resolve, reject) => {
//         cloudant.getAllDbs()
//             .then(body => {
//                 resolve({ dbs: body.result });
//             })
//             .catch(err => {
//                     console.log(err);
//                 reject({ err: err });
//             });
//     });
// }


// /*
// Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
// eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
// */
// function getMatchingRecords(cloudant,dbname, selector) {
//     return new Promise((resolve, reject) => {
//         cloudant.postFind({db:dbname,selector:selector})
//                 .then((result)=>{
//                   resolve({result:result.result.docs});
//                 })
//                 .catch(err => {
//                    console.log(err);
//                     reject({ err: err });
//                 });
//          })
// }

                       
// /*
// Sample implementation to get all the records in a db.
// */
// function getAllRecords(cloudant,dbname) {
//     return new Promise((resolve, reject) => {
//         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
//             .then((result)=>{
//               resolve({result:result.result.rows});
//             })
//             .catch(err => {
//                console.log(err);
//                reject({ err: err });
//             });
//         })
// }
