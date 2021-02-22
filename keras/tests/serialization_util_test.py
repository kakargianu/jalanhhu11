# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for serialization functions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf

import json
from keras import combinations
from keras import keras_parameterized
from keras.engine import input_layer
from keras.engine import sequential
from keras.engine import training
from keras.layers import core
from keras.saving.saved_model import json_utils


@combinations.generate(combinations.combine(mode=["graph", "eager"]))
class SerializationTests(keras_parameterized.TestCase):

  def test_serialize_dense(self):
    dense = core.Dense(3)
    dense(tf.constant([[4.]]))
    round_trip = json.loads(json.dumps(
        dense, default=json_utils.get_json_type))
    self.assertEqual(3, round_trip["config"]["units"])

  def test_serialize_sequential(self):
    model = sequential.Sequential()
    model.add(core.Dense(4))
    model.add(core.Dense(5))
    model(tf.constant([[1.]]))
    sequential_round_trip = json.loads(
        json.dumps(model, default=json_utils.get_json_type))
    self.assertEqual(
        # Note that `config['layers'][0]` will be an InputLayer in V2
        # (but not in V1)
        5, sequential_round_trip["config"]["layers"][-1]["config"]["units"])

  def test_serialize_model(self):
    x = input_layer.Input(shape=[3])
    y = core.Dense(10)(x)
    model = training.Model(x, y)
    model(tf.constant([[1., 1., 1.]]))
    model_round_trip = json.loads(
        json.dumps(model, default=json_utils.get_json_type))
    self.assertEqual(
        10, model_round_trip["config"]["layers"][1]["config"]["units"])

if __name__ == "__main__":
  tf.test.main()