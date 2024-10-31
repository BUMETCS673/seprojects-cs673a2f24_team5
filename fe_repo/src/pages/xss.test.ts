import { expect, test } from 'vitest';
import xss from 'xss';

test('Translate the <> around the script to &lt and &gt', () => {
  const strIncludingScript = xss('<script type="text/javascript">alert(/xss/);</script>');
  expect(strIncludingScript)
    .toEqual('&lt;script type="text/javascript"&gt;alert(/xss/);&lt;/script&gt;');
});

