# Loglar

| Papka | Nima saqlanadi |
|---|---|
| `training/` | Router LoRA o'qitish loglari + natijalar (router_results.json) |
| `inference/` | Server loglari (srv_*.log), download loglari (dl_*.log), orchestrator loglari, benchmark JSONlari |
| `errors/` | Xatolar (kelajakda avtomatik yozish uchun) |

## Muhim loglar

| Fayl | Tavsif |
|---|---|
| `inference/orchestrator.log` | Joriy orchestrator (src.orchestrator.app) |
| `training/router_results.json` | LoRA o'qitish yakuniy metrikalari |
| `inference/hybrid_router_results.json` | Gibrid router threshold taqqoslash |
| `inference/e2e_results.json` | 20 savol E2E benchmark |
| `inference/semantic_router_results.json` | Semantic router (A/B konfiguratsiya) |
