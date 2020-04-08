interface ISourceSetting {
  name: string
  link: string
}

import './settings-page.scss'

export class SettingsPage {
  public message: string = 'Learn some Vocabs';

  private sourceSettings: ISourceSetting[] = [
    { name: 'foo', link: 'https://hello-world.io' },
    { name: 'bar', link: 'https://say-nice-things.io' },
    { name: 'baz', link: 'https://vocab-app.io' },
  ]

  private selectedSourceSetting: ISourceSetting;
}
