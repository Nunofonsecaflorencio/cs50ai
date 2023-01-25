# Read Images
os - module for browse folder and files
cv2 - to read image

# Model

1.

Layers:
- Rescaling [0..255] to [0..1]
- Conv 32 filters 5x5
- MaxPooling 2x2
- Flatten
- 128 unit hidden
- 0.2 dropout
- output 43 units

Results: loss = 0.1350, accuracy = 0.9668

2.

Layers:
- Rescaling [0..255] to [0..1]
- Conv 12 filters 5x5
- MaxPooling 2x2
- Conv 24 filters 5x5
- MaxPooling 2x2
- Flatten
- 120 unit hidden
- 40 unit hidden
- 0.2 dropout
- output 43 units

Results: loss = 0.1114, accuracy = 0.9720

3.

Layers:
- Rescaling [0..255] to [0..1]
- Conv 32 filters 3x3
- MaxPooling 2x2
- Conv 16 filters 3x3
- MaxPooling 2x2
- Flatten
- 128 unit hidden
- 0.2 dropout
- output 43 units

Results: loss = 0.1027, accuracy = 0.9762