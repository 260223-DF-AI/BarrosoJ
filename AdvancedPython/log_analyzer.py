from decorators import timer, logger, cache
from generators import read_lines, batch, filter_errors, filter_by_field
from pipeline import create_pipeline

from collections import defaultdict, Counter

@timer
@logger
def analyze_logs(log_path):
    """
    Analyze a log file and return statistics.
    
    Uses generators for memory-efficient processing.
    Uses decorators for timing and logging.
    """
    
    info_errs, warning_errs, error_errs = count_by_level(log_path)
    log_report: str = f"""Logging counts by level for {log_path}:
INFO: {info_errs}, WARNING: {warning_errs}, ERROR: {error_errs}

Top error messages: {get_error_summary(log_path, top_n=3)}"""

    return log_report


@cache(max_size=1000)
def parse_log_line(line: str) -> dict:
    """
    Parse a single log line into structured data.
    Cached because the same line format appears often.
    """
    date, time, log_level, *msg = line.split(" ")

    line_info: dict = {
        "date": date,
        "time": time,
        "log_level": log_level,
        "message": " ".join(msg)
    }
    return line_info


def count_by_level(log_path: str) -> tuple:
    """
    Count log entries by level (INFO, WARNING, ERROR).
    Use generators to process without loading entire file.
    """
    log_counts: defaultdict[str, int] = defaultdict(int)
    for line in read_lines(log_path):
        parsed_line: dict = parse_log_line(line)
        log_level: str = parsed_line["log_level"]
        log_counts[log_level] += 1

    return (log_counts["INFO"], log_counts["WARNING"], log_counts["ERROR"])

    
def get_error_summary(log_path, top_n=10):
    """
    Get top N most common error messages.
    """
    # parse log file lines
    parsed_lines: list[dict] = []
    for line in read_lines(log_path):
        parsed_lines.append(parse_log_line(line))
    
    # count number of times each error message appears
    error_msg_counts: defaultdict[str, int] = defaultdict(int)
    for error in filter_by_field(parsed_lines, "log_level", "ERROR"):
        error_msg: str = error["message"]
        error_msg_counts[error_msg] += 1

    # use counter to sort error_msg_counts values / for most_common method
    error_msg_counter = Counter(error_msg_counts)
    top_errors: list[tuple[str, int]] = error_msg_counter.most_common(top_n)

    # only return the error message for each top-occurring error
    return [error_tuple[0] for error_tuple in top_errors]
    

def process_logs_in_batches(log_path, batch_size=1000):
    """
    Process logs in batches for database insertion.
    Yields batches of parsed log entries.
    """
    
    for line_batch in batch(list(read_lines(log_path)), batch_size):
        # using batch generator to yield batches of lines
        parsed_batch: list[dict] = [parse_log_line(line) for line in line_batch]
        yield parsed_batch


if __name__ == "__main__":
    # for line in read_lines("samples/app.log"):
    #     print(parse_log_line(line))

    # print(get_error_summary("samples/app.log"))
    analyze_logs("samples/app.log")