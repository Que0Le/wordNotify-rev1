import { IJsonEditor } from 'common/components/json-tree/json-tree';
import * as vocabConfig from '../../../../config.json';
import { httpClient } from './../../common/http-client';

import './settings-page.scss'

export class SettingsPage {
  public vocabConfig: typeof vocabConfig;

  public jsonEditor: IJsonEditor;

  private httpClient = httpClient;

  async created() {
    console.log("TCL: httpClient", httpClient)
    const settingsResponse = (await this.httpClient.fetch('/resources/settings')) as unknown as typeof vocabConfig
    this.vocabConfig = settingsResponse;
  }

  private async saveSettings() {
    const saveResponse = (await this.httpClient.fetch('/resources/settings', {
      method: 'POST',
      body: JSON.stringify(this.jsonEditor.get()),
    })) as unknown as typeof vocabConfig;
  }
}
