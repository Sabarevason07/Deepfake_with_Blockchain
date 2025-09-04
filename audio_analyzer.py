import os
import librosa
import numpy as np
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def build_model(input_shape):
    model = Sequential([
        Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # binary classification: real (0) vs fake (1)
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def analyze_audio(audio_path):
    try:
        # Load audio file with a fixed sampling rate
        y, sr = librosa.load(audio_path, sr=22050)
        if y.size == 0:
            raise ValueError("Empty audio signal")

        # Compute mel spectrogram (shape: (n_mels, t))
        melspec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        # Convert to log scale (dB)
        log_melspec = librosa.power_to_db(melspec, ref=np.max)
        # Normalize spectrogram to [0, 1]
        normalized_spec = (log_melspec - log_melspec.min()) / (log_melspec.max() - log_melspec.min())
        
        # Resize or pad/truncate to fixed time dimension (128 frames)
        if normalized_spec.shape[1] < 128:
            pad_width = 128 - normalized_spec.shape[1]
            normalized_spec = np.pad(normalized_spec, ((0, 0), (0, pad_width)), mode='constant')
        else:
            normalized_spec = normalized_spec[:, :128]
        
        # Expand dimensions: (128, 128, 1) for CNN input
        normalized_spec = np.expand_dims(normalized_spec, axis=-1)
        # Create batch dimension: (1, 128, 128, 1)
        input_data = np.expand_dims(normalized_spec, axis=0)
        
        # Load a pre-trained model if available, else build a new one
        model_path = 'audio_model.h5'
        if os.path.exists(model_path):
            model = load_model(model_path)
        else:
            input_shape = (128, 128, 1)
            model = build_model(input_shape)
            # WARNING: This new model is untrained so predictions will be random.
        
        # Predict deepfake probability (output between 0 and 1)
        prob = model.predict(input_data)[0][0]
        # Convert probability to a percentage (accuracy)
        audio_accuracy = prob * 100
        return int(audio_accuracy)
    except Exception as e:
        print(f"Error in audio analysis: {e}")
        return 50  # Fallback value if processing fails
