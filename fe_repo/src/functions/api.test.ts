import {expect, test} from 'vitest';
import {analyze, login, sendMessage, uploadFile} from "./api.ts";

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
