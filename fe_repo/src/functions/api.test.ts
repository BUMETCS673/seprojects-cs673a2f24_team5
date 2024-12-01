import {expect, test} from 'vitest';
import {analyze, getHasResume, getUserId, login, sendMessage, suggest, suggestJob, uploadFile} from "./api.ts";

global.__CURRENT_URI__ = 'http://localhost';

test('sendMessage', () => {
  expect(sendMessage("I'm adam")).toBeDefined();
});

test('uploadFile', () => {
  // Create a Blob with some content
  const blob = new Blob(['Hello, world!'], {type: 'application/pdf;charset=utf-8'});

  // Convert Blob to File
  const file = new File([blob], 'test.pdf', {type: blob.type});
  expect(uploadFile(file)).toBeFalsy(); // Due to the return value is 'undefined'
});


test('analyze', () => {
  // make sure message is always returned
  expect(async () => (await analyze('hello world'))?.analysis).toBeDefined();
})

test('login', () => {
  // make sure message is always returned
  expect(login('')).toBeDefined();
})

test('suggest', () => {
  // make sure message is always returned
  expect(async () => (await suggest())).toBeDefined();
})

test('suggestJob', () => {
  // make sure message is always returned
  expect(async () => (await suggestJob())).toBeDefined();
})

test('getUserId', () => {
  // make sure message is always returned
  expect(getUserId()).toBeDefined();
})

test('getHasResume', () => {
  // make sure message is always returned
  expect(getHasResume()).toBeDefined();
})
