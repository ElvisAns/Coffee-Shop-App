/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-f-c9bg6g.us', // the auth0 domain prefix
    audience: 'https://127.0.0.1:8100', // the audience set for the auth0 app
    clientId: 'b4HcPNHQv60YYwxdTcV4vPFTnFoRsnft', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
