uniform const vec2 ScreenCenter = vec2(0.5, 0.5);
uniform const float Cone = 6.0;
uniform const float LengthModificator = 1.4;

uniform const int ShadowSamples = 50;
uniform const float ShadowStep = 0.008;

float rand() {
    return fract(sin(iTime) * 100);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord / iResolution.xy;
    vec2 mouse_uv = iMouse.xy / iResolution.xy;

    vec2 center = uv - ScreenCenter;
    vec2 ray_direction = mouse_uv - ScreenCenter;

    float power = pow(dot(normalize(center), normalize(ray_direction)), Cone);
    float light = mix(0.2, power, 1 - length(center) * LengthModificator);

    float shadow = 0.0;
    if(power > 0 && texture(iChannel0, uv).a == 0) {
        for (int i = 0; i < ShadowSamples; i++) {
            vec2 pv = uv - (i * ShadowStep * normalize(ray_direction));
            if(dot(normalize(ray_direction), normalize(pv - ScreenCenter)) > 0)
                shadow += texture(iChannel0, pv).a / ShadowSamples;
        }
    }

    fragColor = mix(vec4(0), texture(iChannel1, uv) * light, 1 - shadow * 2.3) * step(0.02, rand() * 10);
}