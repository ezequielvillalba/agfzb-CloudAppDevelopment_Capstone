/**
 * Get all databases
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

if (require.main === module) {
    var params = {
        COUCH_URL: process.env.COUCH_URL,
        IAM_API_KEY: process.env.IAM_API_KEY,
        COUCH_USERNAME: process.env.COUCH_USERNAME
    };

    main(params);
}

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbList = getDbs(cloudant);
    return { dbs: dbList };
}

function getDbs(cloudant) {
    cloudant.getAllDbs().then((body) => {
        body.forEach((db) => {
            dbList.push(db);
        });
    }).catch((err) => { console.log(err); });
}

