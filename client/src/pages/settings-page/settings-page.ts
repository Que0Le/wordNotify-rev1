import * as vocabConfig from '../../../../config.json';
import { httpClient } from './../../common/http-client';

interface ISourceSetting {
  name: string
  search_url: string
}

import './settings-page.scss'

export class SettingsPage {
  public message: string = 'Learn some Vocabs';

  private sourceSettings: ISourceSetting[] = [
    { name: 'foo', search_url: 'https://hello-world.io' },
    { name: 'bar', search_url: 'https://say-nice-things.io' },
    { name: 'baz', search_url: 'https://vocab-app.io' },
  ]

  private selectedSourceSetting: ISourceSetting;

  private vocabConfig: typeof vocabConfig;

  private httpClient = httpClient;

  async bind() {
    const settingsResponse = (await this.httpClient.fetch('/resources/settings')) as unknown as typeof vocabConfig
    this.vocabConfig = settingsResponse;
    this.vocabConfig.online_sources
    this.vocabConfig.online_sources[0].search_url
    this.vocabConfig.system_notification.duration_sec
    this.vocabConfig.system_notification.interval_sec

  }

  private async saveSettings() {
    const saveResponse = (await this.httpClient.fetch('/resources/settings', {
      method: 'POST',
      body: JSON.stringify(this.vocabConfig),
    })) as unknown as typeof vocabConfig;
  }
}
