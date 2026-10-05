import unittest
from unittest.mock import Mock
from deepseek_api import DeepSeekAPI, DeepSeekAPIError, MODEL_ID

class TestClient(unittest.TestCase):
    def make(self, status=200, payload=None):
        s=Mock(); r=Mock(status_code=status); r.json.return_value=payload or {"id":"r1","choices":[]}; s.post.return_value=r; return s
    def test_model_and_effort(self):
        s=self.make(); DeepSeekAPI('key',session=s).chat([{"role":"user","content":"hi"}],reasoning_effort='low'); body=s.post.call_args.kwargs['json']; self.assertEqual(body['model'],MODEL_ID); self.assertEqual(body['reasoning_effort'],'low')
    def test_bad_effort(self):
        with self.assertRaises(DeepSeekAPIError): DeepSeekAPI('key',session=self.make()).chat([{"role":"user","content":"hi"}],reasoning_effort='none')
    def test_http_error(self):
        with self.assertRaises(DeepSeekAPIError) as ctx: DeepSeekAPI('key',session=self.make(401,{"error":"bad"})).chat([{"role":"user","content":"hi"}])
        self.assertEqual(ctx.exception.status_code,401)
if __name__=='__main__': unittest.main()
