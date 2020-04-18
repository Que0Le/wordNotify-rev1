import { HttpClient, json } from 'aurelia-fetch-client';
import * as appConfigDefault from '../../app-config.json';

const appConfig = JSON.parse(JSON.stringify(appConfigDefault)).default as unknown as typeof appConfigDefault
const { Authorization, baseUrl } = appConfig;

const offlineMode = true

export const httpClient = offlineMode ? new HttpClient() : {
  configure: () => { },
  fetch: () => { },
  isRequesting: false
};

httpClient.configure(config => {
  config
    .withBaseUrl(baseUrl || 'api/v1')
    .withDefaults({
      credentials: 'same-origin',
      headers: {
        'Accept': 'application/json',
        Authorization,
        'Content-Type': 'application/json',
        'X-Requested-With': 'Fetch',
      }
    })
    .withInterceptor({
      request(request) {
        console.log(`Requesting ${request.method} ${request.url}`);
        return request;
      },
      response(response) {
        console.log(`Received ${response.status} ${response.url}`);
        return response.json();
      }
    });
});
