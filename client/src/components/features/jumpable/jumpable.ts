const DEBUG_MODE = {
  persistJumpable: true
};

import hotkeys from 'hotkeys-js';
import './jumpable.scss';

let keyBinding = hotkeys.noConflict() as any;
hotkeys.filter = function () { return true; }; // 2018-08-09 23:30:46 what does this do?

let isPERSISTENT = DEBUG_MODE.persistJumpable;
let isJumpable = true;

const JUMP_CLASS = 'jumpable';
const DATA_JUMP_MARK_VALUE = 'data-jump-mark-value';
const ABC = [
  't', 'n', 'h', 'e', 's', 'o', 'a', 'g', 'y', // home row
  'r', 'u', 'p', 'd', 'p', // upper
  'c', 'm', 'l', 'q', ';', // lower
  '1', '2', '3', '4', '5', '6', '7', '8', '9', '0' // numbers
  // "ff", "fj", "fd", "fk", "fs", "fl", "fa", "fg", "fh", // f + home row
];

const ABC_leftHandOnly = [
  't', 'h', 's', 'a', 'g', // home row
  'r', 'd', // upper
  'c', 'm', 'q', // lower
  // "ff", "fj", "fd", "fk", "fs", "fl", "fa", "fg", "fh", // f + home row

];

// const ABC_qwerty = [
//   'f', 'j', 'd', 'k', 's', 'l', 'a', 'g', 'h', // home row
//   'e', 'i', 'o', 'w', 'n', // upper
//   'v', 'c', 'm', 'q', 'p', // lower
//   '1', '2', '3', '4', '5', '6', '7', '8', '9', '0' // numbers
// ];

const ABC_JOINED = ABC_leftHandOnly.join(', ');
const ABC_GEN = ABC_leftHandOnly;

const blackList = [
  'input'
];

/**
 * Refresh by deleting old listener and attach new one
 */
export function refreshJumpable() {
  const destroy = makeTagsJumpable();
  jumpableKeyCodesListener(destroy);
}

/**
 * @param {CSSSelector:<String>} context - In order to restrict jumpy, defaults to body, ie. #hio-body
 */
export const toggleJumpable = (context = '#hio-body') => {
  // let jumpContext = document.querySelectorAll(context);
  // for (let iterator of jumpContext) {
  //   let jumpLocations = iterator.getElementsByClassName(JUMP_CLASS);
  // }

  const destroy = makeTagsJumpable();
  isJumpable ?
    jumpableKeyCodesListener(destroy)
    : destroyKeybinding(destroy);
};

/**
 * Iterate through list of tags and add `JUMP_CLASS` to these tags.
 * @param {[HTMLTag:<String>]} tagNames
 * @returns {Function | Function[]} destroy - Function to deactivate jumpable ability.
 */
const makeTagsJumpable = (tagNames = ['a', 'button', 'label']) => {
  let uniqueJumpMark = getUniqueJumpMarkGenerator();
  let destroyCollector: any[] = [];

  const destroy = (taggels: HTMLCollectionOf<HTMLElement>) => {
    return () => {
      for (let taggel of taggels) {
        taggel.classList.remove(JUMP_CLASS);
        taggel.setAttribute(DATA_JUMP_MARK_VALUE, '');
      }
    };
  };

  tagNames.forEach((tag) => {
    let taggels = document.getElementsByTagName(tag) as HTMLCollectionOf<HTMLElement>;
    for (let taggel of taggels) {
      taggel.classList.add(JUMP_CLASS);
      let value = uniqueJumpMark.next().value || '';
      taggel.setAttribute(DATA_JUMP_MARK_VALUE, value);
    }

    destroyCollector.push(destroy(taggels));
  });

  return destroyCollector;
};

/**
 * Return unique jump mark value to be displayed.
 */
function* getUniqueJumpMarkGenerator() {
  yield* ABC_GEN;
}

/**
 * When jumpable is activated, listen to key presses to actually jump.
 */
const jumpableKeyCodesListener = (destroy: any) => {
  keyBinding(ABC_JOINED, JUMP_CLASS, (ev: any) => {
    let pressedKey = ev.key;
    let jumppelIterable = document.getElementsByClassName(JUMP_CLASS);
    const activate = activateElement(destroy);
    activate(jumppelIterable, pressedKey);
  });

  keyBinding('enter', JUMP_CLASS, () => { // Why ENTER here?
    hotkeys.deleteScope(JUMP_CLASS);
    hotkeys.unbind(ABC_JOINED);
    hotkeys.unbind('enter');
  });

  hotkeys.setScope(JUMP_CLASS);
};

function checkActiveItemBlackList() {
  const { activeElement } = document;
  if (activeElement === null) return;

  // Root source: list item with text div is contenteditable
  const isContentEditable = activeElement.getAttribute('contenteditable');
  if (isContentEditable) return true;

  const activeTag = activeElement.tagName.toLocaleLowerCase();
  return blackList.includes(activeTag);
}

/**
 * When pressed key is equal to jump mark, perform a click on that element
 * @param {Function} cb - If given, perform after jumped (eg. destroy listener)
 * @param {String} activation - Specify how the jumppel should be activated
 * @returns {Function} action
 *  * @param {HTML.Collection} jumppelIterable
 *  * @param {String} pressedKey
 */
const activateElement = (cb: Function, activation = 'click') => {
  const action = (jumppelIterable: any, pressedKey: any) => {
    for (let jumppel of jumppelIterable) {
      let attr = jumppel.getAttribute(DATA_JUMP_MARK_VALUE);
      if (checkActiveItemBlackList()) return;
      if (attr === pressedKey) {
        switch (activation) {
          default:
            jumppel.click();
            isJumpable = false;
        }
        destroyKeybinding(cb); // FIXME: now, we just accumulate listeners
        refreshJumpable();
      }
    }
  };
  return action;
};

/**
 *
 * @param {Function} cb - Callback to deactivate jump ability
 */
function destroyKeybinding(cb: Function | Function[]) {
  if (typeof cb === 'function') {
    cb();
    hotkeys.deleteScope(JUMP_CLASS);
  } else if (Array.isArray(cb)) {
    cb.forEach((callback) => {
      callback();
      hotkeys.deleteScope(JUMP_CLASS);
    });
  }
}

export function togglePersistJumpable() {
  isPERSISTENT = !isPERSISTENT; // This is bugged for turning off toggel EyeRR_b8B
  // isPERSISTENT ? hotkeys.setScope(JUMP_CLASS) : '';
  hotkeys.setScope(JUMP_CLASS);
}
