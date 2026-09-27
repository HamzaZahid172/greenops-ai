import logging
import time
import uuid

from fastapi import Request

from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from app.observability.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
)


logger = logging.getLogger(
    "greenops.requests"
)


class ObservabilityMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        request_id = (
            request.headers.get(
                "X-Request-ID"
            )
            or str(uuid.uuid4())
        )

        started = time.perf_counter()

        try:
            response = await call_next(
                request
            )

            status_code = (
                response.status_code
            )

        except Exception:
            duration = (
                time.perf_counter()
                - started
            )

            route = request.url.path

            HTTP_REQUESTS_TOTAL.labels(
                method=request.method,
                route=route,
                status="500",
            ).inc()

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=request.method,
                route=route,
            ).observe(duration)

            logger.exception(
                "request_failed "
                "request_id=%s "
                "method=%s "
                "path=%s "
                "duration_ms=%.2f",
                request_id,
                request.method,
                request.url.path,
                duration * 1000,
            )

            raise


        duration = (
            time.perf_counter()
            - started
        )

        route_object = (
            request.scope.get("route")
        )

        route = getattr(
            route_object,
            "path",
            request.url.path,
        )


        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            route=route,
            status=str(status_code),
        ).inc()


        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            route=route,
        ).observe(duration)


        response.headers[
            "X-Request-ID"
        ] = request_id


        logger.info(
            "request_complete "
            "request_id=%s "
            "method=%s "
            "path=%s "
            "status=%s "
            "duration_ms=%.2f",
            request_id,
            request.method,
            route,
            status_code,
            duration * 1000,
        )


        return response