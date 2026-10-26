import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';

const require=createRequire(import.meta.url);
const sockjsRequire=createRequire(require.resolve('sockjs'));
test('patched UUID preserves the CommonJS interface used by the development server',()=>{
 const sockjs=require('sockjs');
 assert.equal(typeof sockjs.createServer().installHandlers,'function');
 const uuid=sockjsRequire('uuid');
 assert.match(uuid.v4(),/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
});
test('UUID rejects an undersized output buffer instead of writing beyond its bounds',()=>{
 const uuid=sockjsRequire('uuid');
 assert.throws(()=>uuid.v3('example',uuid.v3.DNS,new Uint8Array(1)),RangeError);
});
