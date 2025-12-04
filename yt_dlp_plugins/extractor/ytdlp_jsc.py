from __future__ import annotations

from yt_dlp.extractor.youtube.jsc.provider import (
    JsChallengeProvider,
    JsChallengeProviderError,
    JsChallengeProviderResponse,
    JsChallengeRequest,
    JsChallengeResponse,
    JsChallengeType,
    NChallengeOutput,
    SigChallengeOutput,
    register_preference,
    register_provider,
)
from yt_dlp.extractor.youtube.pot._provider import BuiltinIEContentProvider

try:
    from ytdlp_jsc import solve as _solve
    _HAS_YTDLP_JSC = True
except ImportError:
    _HAS_YTDLP_JSC = False
    _solve = None


__version__ = '0.1.0'


@register_provider
class YtdlpJscJCP(JsChallengeProvider, BuiltinIEContentProvider):
    """JS Challenge Provider using ytdlp-jsc library"""
    PROVIDER_NAME = 'ytdlp-jsc'
    PROVIDER_VERSION = __version__
    BUG_REPORT_LOCATION = 'https://github.com/yt-dlp/yt-dlp/issues'

    _SUPPORTED_TYPES = [JsChallengeType.N, JsChallengeType.SIG]

    def is_available(self) -> bool:
        return _HAS_YTDLP_JSC

    def _real_bulk_solve(self, requests: list[JsChallengeRequest]):
        if not requests:
            return

        # Group requests by player_url
        grouped: dict[str, list[JsChallengeRequest]] = {}
        for request in requests:
            player_url = request.input.player_url
            if player_url not in grouped:
                grouped[player_url] = []
            grouped[player_url].append(request)

        for player_url, group_requests in grouped.items():
            # Download player.js
            video_id = next((r.video_id for r in group_requests if r.video_id), None)
            try:
                player_js = self._get_player(video_id, player_url)
            except JsChallengeProviderError as e:
                for request in group_requests:
                    yield JsChallengeProviderResponse(request=request, error=e)
                continue

            self.logger.info('Solving JS challenges using ytdlp-jsc')

            # Process each request
            for request in group_requests:
                try:
                    result = self._solve_request(player_js, request)
                    yield JsChallengeProviderResponse(request=request, response=result)
                except JsChallengeProviderError as e:
                    yield JsChallengeProviderResponse(request=request, error=e)

    def _solve_request(self, player_js: str, request: JsChallengeRequest) -> JsChallengeResponse:
        """Solve a single challenge request"""
        challenge_type = request.type.value  # 'n' or 'sig'
        challenges = request.input.challenges
        results = {}

        for challenge in challenges:
            try:
                result = _solve(player_js, challenge_type, challenge)
                if not result:
                    raise JsChallengeProviderError(f'ytdlp-jsc returned empty result for {challenge_type}:{challenge}')
                results[challenge] = result
            except Exception as e:
                if isinstance(e, JsChallengeProviderError):
                    raise
                raise JsChallengeProviderError(f'ytdlp-jsc solve failed: {e}') from e

        if request.type == JsChallengeType.N:
            return JsChallengeResponse(type=request.type, output=NChallengeOutput(results=results))
        else:
            return JsChallengeResponse(type=request.type, output=SigChallengeOutput(results=results))


@register_preference(YtdlpJscJCP)
def preference(provider: JsChallengeProvider, requests: list[JsChallengeRequest]) -> int:
    return 1111
