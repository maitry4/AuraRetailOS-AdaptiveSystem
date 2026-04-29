from failure.failure_handler import FailureHandler

class AutoRetryHandler(FailureHandler):
    """
    <<Concrete Handler 1>>
    Attempts to retry the operation up to 3 times for transient errors.
    """
    MAX_RETRIES = 3

    def handle(self, failure_context: dict) -> bool:
        error_code = failure_context.get("error_code", "UNKNOWN")
        retry_count = failure_context.get("retry_count", 0)

        if "TRANSIENT" in error_code and retry_count < self.MAX_RETRIES:
            print(f"  [AutoRetry] Transient error '{error_code}' detected. Retry {retry_count + 1}/{self.MAX_RETRIES}...")
            failure_context["retry_count"] = retry_count + 1
            # In a real system, we would trigger the actual retry here.
            # For demo, we simulate a successful retry on the 2nd attempt.
            if failure_context["retry_count"] == 2:
                print("  [AutoRetry] V Retry successful.")
                return True
            
        print(f"  [AutoRetry] Could not resolve '{error_code}'. Passing to next handler.")
        return super().handle(failure_context)
