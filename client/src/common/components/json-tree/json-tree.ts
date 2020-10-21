import { bindable } from 'aurelia-framework';
import JSONEditor from 'jsoneditor';
import 'jsoneditor/dist/jsoneditor.min.css';

export interface IJsonEditor {
  expandAll: () => {},
  get: () => {},
  set: (anObject: any) => {},
}

/**
 * ## Api Doc
 * https://github.com/josdejong/jsoneditor/blob/master/docs/api.md
 *
 * ## Demo
 * http://jsoneditoronline.org/#left=local.lusobu&right=local.wexaci
 */
export class JsonTree {

  @bindable jsonData: any;

  @bindable jsonEditor: JSONEditor;

  private jsonEditorRef: HTMLDivElement;

  attached() {
    const options = {};
    this.jsonEditor = new JSONEditor(this.jsonEditorRef, options)

    const initialJson = {
      "Array": [1, 2, 3],
      "Boolean": true,
      "Null": null,
      "Number": 123,
      "Object": { "a": "b", "c": "d" },
      "String": "Hello World"
    }
    this.jsonEditor.set(this.jsonData || initialJson)
  }

  printJsonToConsole() {
    console.log("JsonTree -> printJsonToConsole -> this.jsonEditor.get()", this.jsonEditor.get())
  }
}
