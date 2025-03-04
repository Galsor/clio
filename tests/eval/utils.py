import datetime
import json
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from pydantic_ai.result import ResultDataT

from tests.eval import EVAL_RESULTS_PATH


@dataclass
class EvalResults:
    run_results: List[ResultDataT]

    @property
    def data(self) -> List[dict]:
        return [r.data.model_dump() for r in self.run_results]

    def save_json(
        self,
        folder_path: os.PathLike = EVAL_RESULTS_PATH,
        file_prefix: Optional[str] = None,
    ):
        if file_prefix is None:
            file_prefix = "EvalResults_data"

        path = (
            Path(folder_path)
            / f"{file_prefix}_{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )

        with open(path, "w", encoding="UTF-8") as f:
            json.dump(self.data, f)

    def save_raw_in_pickle(
        self,
        folder_path: os.PathLike = EVAL_RESULTS_PATH,
        file_prefix: Optional[str] = None,
    ):
        if file_prefix is None:
            file_prefix = "EvalResults"

        path = (
            Path(folder_path)
            / f"{file_prefix}_{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S')}.pkl"
        )

        with open(path, "wb") as f:
            pickle.dump(self.run_results, f)
